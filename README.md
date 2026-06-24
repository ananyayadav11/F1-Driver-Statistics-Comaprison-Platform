# F1 Dashboard
 
A full-stack Formula 1 analytics website featuring live driver standings, head-to-head driver comparison, and a machine learning model that predicts race finishing positions for every driver on the grid.
 
---
 
<img width="1882" height="951" alt="Screenshot 2026-02-08 140536" src="https://github.com/user-attachments/assets/a278e935-9f21-4c42-bf74-3bdca1dfbf7e" />
<img width="928" height="503" alt="image" src="https://github.com/user-attachments/assets/e7c27be1-3af7-4907-bc99-fa54b221a6b6" />
<img width="887" height="485" alt="image" src="https://github.com/user-attachments/assets/a6232712-f731-4c56-be2a-608c9f3562d9" />
<img width="920" height="521" alt="image" src="https://github.com/user-attachments/assets/b39cc048-b534-4f13-92c9-3907123b93d5" />

---
 
## Features
 
- **Driver Standings** — Live 2025 championship standings fetched from the Jolpica F1 API including position, points, team, and nationality
- **Driver Cards** — Visual cards for  F1 drivers with team colors
- **Driver Comparison** — Head-to-head comparison of any two drivers showing points, wins, championship position, and points difference
- **Race Prediction** — ML model predicting the full finishing order (P1 to P20) for any historical race in the dataset
- **News Section** — Curated F1 news cards
---
 
## Tech Stack
 
**Frontend**
- HTML, CSS, JavaScript
- Tailwind CSS
  
**Backend**
- Python
- FastAPI
- Uvicorn
**Machine Learning**
- FastF1 (data collection)
- Pandas, NumPy (data processing)
- XGBoost (prediction model)
- Scikit-learn (preprocessing, evaluation)
- Joblib (model serialization)
  
**APIs**
- Jolpica F1 API (live standings and driver data)
- FastF1 (historical race data)
---
 
## Project Structure
 
```
f1_dashboard/
├── app.py                  # FastAPI backend
├── collect_data.py         # FastF1 data collection script
├── data_cleaning.ipynb     # Data cleaning, feature engineering, model training
├── index.html              # Frontend
├── 11.js                   # Frontend logic
├── f1.images/              # Driver and flag images
└── README.md
```
 
---
 
## ML Model
 
The race prediction model is built using XGBoost Regressor trained on 5 years of historical F1 data (2020-2024) collected via the FastF1 library.
 
**Data collected:** 148,648 lap records across 98 races
 
**Features used:**
- Average lap time per driver per race
- Best lap time per driver per race
- Lap time consistency (standard deviation)
- Total laps completed
- Grid (qualifying) position
- Constructor (team)
- Driver
- Circuit
**Target:** Final race finishing position (P1 to P20)
 
**Result:** Mean Absolute Error of 2.27 positions — meaning predictions are accurate to within approximately 2 finishing places on average.
 
---
 
## API Endpoints
 
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/standings | Live 2025 driver championship standings |
| GET | /api/drivers | All current F1 drivers |
| POST | /api/compare | Head-to-head driver comparison |
| GET | /api/predict-podium | ML predicted finishing order |
| GET | /api/health | Health check |
 
---
 
## Running Locally
 
1. Install dependencies
```bash
pip install fastapi uvicorn pandas numpy scikit-learn xgboost fastf1 joblib requests
```
 
2. Start the backend
```bash
uvicorn app:app --reload
```
 
3. Open `index.html` in your browser
---
 
## Notes
 
- The prediction model uses historical race data (2020-2024). Predictions reflect patterns learned from past races including grid position, team performance, and driver consistency.
- Live standings are fetched in real time from the Jolpica F1 API.
- News section is currently static.
 
  
