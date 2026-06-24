from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import requests

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load model and encoders
model=joblib.load('model.pkl')
le_driver=joblib.load('le_driver.pkl')
le_race=joblib.load('le_race.pkl')
le_team=joblib.load('le_team.pkl')
features=pd.read_csv('data/f1_features_final.csv')

JOLPICA_BASE='https://api.jolpi.ca/ergast/f1'

@app.get("/api/health")
def health():
    return {"status":"healthy"}

@app.get("/api/drivers")
def get_drivers():
    try:
        res=requests.get(f"{JOLPICA_BASE}/2025/drivers.json")
        data=res.json()
        drivers=data['MRData']['DriverTable']['Drivers']
        result=[{
            "id":d['driverId'],
            "firstName":d['givenName'],
            "lastName":d['familyName'],
            "nationality":d['nationality'],
            "code":d.get('code','')
        } for d in drivers]
        return {"success":True,"data":result}
    except Exception as e:
        return {"success":False,"error":str(e)}

@app.get("/api/standings")
def get_standings():
    try:
        res=requests.get(f"{JOLPICA_BASE}/2025/driverStandings.json")
        data=res.json()
        standings=data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        result=[{
            "position":int(s['position']),
            "driverId":s['Driver']['driverId'],
            "firstName":s['Driver']['givenName'],
            "lastName":s['Driver']['familyName'],
            "nationality":s['Driver']['nationality'],
            "team":s['Constructors'][0]['name'],
            "points":float(s['points']),
            "wins":int(s['wins'])
        } for s in standings]
        return {"success":True,"data":result}
    except Exception as e:
        return {"success":False,"error":str(e)}

@app.post("/api/compare")
async def compare_drivers(body:dict):
    try:
        driver1_id=body.get('driver1')
        driver2_id=body.get('driver2')

        res=requests.get(f"{JOLPICA_BASE}/2025/driverStandings.json")
        data=res.json()
        standings=data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        def find_driver(driver_id):
            for s in standings:
                if s['Driver']['driverId']==driver_id:
                    return {
                        "name":f"{s['Driver']['givenName']} {s['Driver']['familyName']}",
                        "team":s['Constructors'][0]['name'],
                        "position":int(s['position']),
                        "points":float(s['points']),
                        "wins":int(s['wins']),
                        "avgPoints":round(float(s['points'])/max(1,int(s['position'])),1)
                    }
            return None

        d1=find_driver(driver1_id)
        d2=find_driver(driver2_id)

        if not d1 or not d2:
            return {"success":False,"error":"Driver not found"}

        return {
            "success":True,
            "data":{
                "driver1":d1,
                "driver2":d2,
                "differences":{
                    "points":d1['points']-d2['points'],
                    "wins":d1['wins']-d2['wins'],
                    "position":d1['position']-d2['position']
                }
            }
        }
    except Exception as e:
        return {"success":False,"error":str(e)}

@app.get("/api/predict-podium")
def predict_podium():
    try:
        # Use latest race in our dataset
        latest_year=features['Year'].max()
        latest_race=features[features['Year']==latest_year]['Race'].iloc[-1]

        race=features[(features['Race']==latest_race)&(features['Year']==latest_year)].copy()

        race_X=race[['AvgLapTime','BestLapTime','Consistency','TotalLaps','Driver_encoded','Race_encoded','Year','GridPosition','Team_encoded']]
        race['PredictedPosition']=model.predict(race_X)
        race['PredictedPosition']=race['PredictedPosition'].rank(method='first').astype(int)

        result=race[['Driver','TeamName','GridPosition','PredictedPosition']].sort_values('PredictedPosition')

        return {"success":True,"data":result.to_dict(orient='records'),"race":latest_race,"year":int(latest_year)}
    except Exception as e:
        return {"success":False,"error":str(e)}