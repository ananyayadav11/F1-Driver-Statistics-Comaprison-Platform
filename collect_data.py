import fastf1
import pandas as pd

# Cache so it doesnt re-download every time
fastf1.Cache.enable_cache('cache')

seasons=[2020,2021,2022,2023,2024]
all_data=[]
for year in seasons:
    try:
        schedule=fastf1.get_event_schedule(year) #to get the race schedule for that year
        for _, event in schedule.iterrows():
            try:
                print(f"Loading {year} - {event['EventName']}")
                        
                session=fastf1.get_session(year,event['EventName'], 'R')
                session.load(telemetry=False,weather=False,messages=False) #since size is too large we are not loding these yet
                laps=session.laps
                        
                df=laps[['Driver','LapTime','LapNumber','Position','Compound','Stint','PitInTime','PitOutTime']].copy() #columns we are using for now
                        
                #race info
                df['Year']=year
                df['Race']=event['EventName']
                df['Circuit']=event['Location']
                        
                all_data.append(df)
            except Exception as e:                     
                print(f"Skipped {event['EventName']} {year} — {e}")
                continue   
    except Exception as e:
        print(f"Skipped entire {year} season — {e}")
        continue
final_df=pd.concat(all_data,ignore_index=True)
final_df.to_csv('data/f1_data.csv',index=False)
print(f"rows: {len(final_df)}")
print(final_df.head(20))