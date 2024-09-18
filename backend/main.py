from datetime import date, timedelta
import math
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import joblib

from DB_interface import Get_data, insert_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can use ["*"] for simplicity but it's less secure
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to predict the days to spoil based on inputs
def predict_days_to_spoil(fruit_name, temperature, humidity, co2_level):
    regressor, ct = joblib.load('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_spoil_model_v2.pkl')
    # Prepare the input data in the same order as the dataset (fruit, temperature, humidity, co2_level)
    input_data = [[fruit_name, temperature, humidity, co2_level]]
    
    # Apply the same One-Hot Encoding transformation used during training
    input_data_transformed = ct.transform(input_data)
    
    # Use the trained model to make a prediction
    predicted_days = regressor.predict(input_data_transformed)
    
    return predicted_days[0]  # Return the predicted number of days


class IoTData(BaseModel):
    temperature: float
    humidity: float
    co2_level: float
    fruit_name: str

@app.post("/process_data")
async def process_data(data: List[IoTData]):
    results = []
    today_date = date.today()

    for item in data:
        try:
            predicted_days = predict_days_to_spoil(item.fruit_name, item.temperature, item.humidity, item.co2_level)
            expiry_date = today_date + timedelta(days=predicted_days)

            result = {
                "Item_name": item.fruit_name, 
                "Production_date": today_date, 
                "Expiry_date": expiry_date
            }
            results.append(result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    insert_data(results)
    
    return results

@app.get("/get_data")
def show_info():
    fetched_data = Get_data()
    return {fetched_data}
