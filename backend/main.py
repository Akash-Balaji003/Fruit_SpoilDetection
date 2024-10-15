import base64
from datetime import date, timedelta
from gc import get_debug
from io import BytesIO
from PIL import Image
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import joblib

from DB_interface import Get_data, get_fruit_records, insert_data_v2, update_expiry_date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can use ["*"] for simplicity but it's less secure
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def predict_days_to_spoil(fruit_name, temperature, humidity, co2_level):
    lr_algo, ct = joblib.load('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_spoil_model_v3.pkl') # Model with oneDAL
    # Transform the input data
    fruit_encoded = ct.transform([[fruit_name.lower(), temperature, humidity, co2_level]])

    # Make the prediction
    predicted_days = lr_algo.predict(fruit_encoded)

    # Print the number of days to spoil
    print(f"Predicted Days to Spoil: {predicted_days[0]:.2f}")

    return predicted_days[0]

def predict_manure_for_methods(fruit_name, waste_weight):
    manure_model = joblib.load('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/Manure_v4.pkl')
    # Load manure dataset (or relevant column data)
    manure_data = pd.read_csv('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/datasets/synthetic_fruit_decomposition_data_1000.csv')  # Using the synthetic dataset

    # Filter the dataset based on the fruit type
    fruit_data = manure_data[manure_data['Fruit Type'] == fruit_name.lower()]

    # Store the results for each method
    results = []

    # Iterate through each method and predict manure weight
    for method in fruit_data['Method'].unique():
        method_data = fruit_data[fruit_data['Method'] == method].iloc[0]
        C_N_ratio = method_data['C:N Ratio']
        time_to_manure = method_data['Time to Manure (weeks)']

        # Use the saved model to predict the manure weight
        prediction = manure_model.predict(pd.DataFrame([[waste_weight, C_N_ratio, time_to_manure]], columns=['Fruit Waste (kg)', 'C:N Ratio', 'Time to Manure (weeks)']))
        predicted_manure_weight = prediction[0]

        # Print the results for each method
        print(f"Method: {method}")
        print(f"Time to manure: {time_to_manure:.1f} weeks")
        print(f"Estimated manure weight: {predicted_manure_weight:.2f} kg")
        print("----------------------------------------")

        results.append({
            'Method': method,
            'Time_to_Manure': time_to_manure,
            'Predicted_Manure_Weight': predicted_manure_weight
        })

    return results

class poster(BaseModel):
    fruit_name: str
    weight: float

@app.post("/poster")
async def poster(data: poster):
    pred = predict_manure_for_methods(data.fruit_name, data.weight)
    return pred

@app.get("/get_data")
def show_info():
    try:
        fetched_data = Get_data()
        return fetched_data  # No need for curly braces, just return the data directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class IoTData(BaseModel):
    temperature: float
    humidity: float
    co2_level: float

# Final version_1
@app.post("/process_data_without_fruit_name")
async def process_data_without_fruit(data: IoTData):
    try:
        # Fetch all fruits
        fruit_records = get_fruit_records()

        if not fruit_records:
            raise HTTPException(status_code=404, detail="No fruit records found")

        today_date = date.today()

        for fruit in fruit_records:
            fruit_name = fruit['item_name']
            fruit_id = fruit['item_id']

            # Predict the number of days until spoilage for this fruit
            predicted_days = predict_days_to_spoil(fruit_name, data.temperature, data.humidity, data.co2_level)

            # Calculate the expiry date
            expiry_date = today_date + timedelta(days=predicted_days)

            # Update the expiry date for the respective fruit in the database
            update_expiry_date(fruit_id, expiry_date)

        return {"message": "Expiry dates updated successfully for all fruits"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Item(BaseModel):
    name: str
    quantity: float
    
@app.post("/initial_storage")
async def submit_items(items: List[Item]):
    data = [{"name": item.name, "quantity": item.quantity} for item in items]
    try:
        insert_data_v2(data)
        return {"message": "Items successfully inserted into the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
