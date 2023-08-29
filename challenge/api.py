from typing import List, Optional
from fastapi import FastAPI
import fastapi
import pandas as pd
from pydantic import BaseModel
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from model import DelayModel

app = FastAPI()

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class FlightList(BaseModel):
    flights: List[Flight]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}

@app.post("/predict", status_code=200)
async def post_predict(flight_list: FlightList) -> dict:
    # Convert input to dataframe
    data = pd.DataFrame([flight.__dict__ for flight in flight_list.flights])
    
    # Check for unknown columns
    opera_values = [
        "Aerolineas Argentinas",
        "Latin American Wings",
        "Grupo LATAM",
        "Sky Airline",
        "Copa Air",
    ]
    tipovuelo_values = ["N", "I"]
    mes_values = list(range(1, 13))
    
    if any(data['OPERA'].apply(lambda x: x not in opera_values)) or \
       any(data['TIPOVUELO'].apply(lambda x: x not in tipovuelo_values)) or \
       any(data['MES'].apply(lambda x: x not in mes_values)):
        return fastapi.Response(content="Unknown column value", status_code=400)
    
    # Preprocess the data
    model = DelayModel()

    features = model.preprocess(data)
    
    # Make predictions
    predictions = model.predict(features)
    return {"predict": predictions}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

