from datetime import date, timedelta
from gc import get_debug
from io import BytesIO
from PIL import Image
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
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

# Function to classify fruit image
def classify_fruit(image: Image.Image):
    # Load the trained model
    fruit_model = tf.keras.models.load_model('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_model_v4.h5')

    img_size = (128, 128)
    image = image.resize(img_size)  # Resize to match model input size
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Predict the fruit class
    predictions = fruit_model.predict(image_array)

    # Check predictions before accessing
    if predictions.size == 0:
        raise HTTPException(status_code=500, detail="Model returned no predictions")

    predicted_class_idx = np.argmax(predictions, axis=1)

    # Ensure predicted_class_idx is valid
    if predicted_class_idx.size == 0:
        raise HTTPException(status_code=500, detail="No valid class predicted")

    # Map predicted class index to fruit names
    fruit_names = ['Apple', 'Banana', 'Grapes', 'Guava', 'HogPlum', 'Jackfruit', 'Litchi', 'Mango', 'Orange', 'Papaya']  # Same order as in class_map
    return fruit_names[predicted_class_idx[0]]



# Function to predict the days to spoil based on inputs
def predict_days_to_spoil(fruit_name, temperature, humidity, co2_level):
    regressor, ct = joblib.load('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_spoil_model_v2.pkl')
    # Prepare the input data in the same order as the dataset (fruit, temperature, humidity, co2_level)
    input_data = [[fruit_name.lower(), temperature, humidity, co2_level]]
    
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

# Endpoint to get input data without image classification (Temporary)
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
    try:
        fetched_data = Get_data()
        return fetched_data  # No need for curly braces, just return the data directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_data_final")
async def process_data_with_image(
    temperature: float = Form(...),
    humidity: float = Form(...),
    co2_level: float = Form(...),
    image: UploadFile = File(...)
):
    results = []

    try:
        # Read the image file
        image_data = await image.read()
        image_pil = Image.open(BytesIO(image_data))

        # Classify the fruit from the image
        fruit_name = classify_fruit(image_pil)

        # Predict days to spoil
        predicted_days = predict_days_to_spoil(fruit_name, temperature, humidity, co2_level)
        
        today_date = date.today()
        expiry_date = today_date + timedelta(days=predicted_days)

        result = {
            "Item_name": fruit_name,
            "Production_date": today_date,
            "Expiry_date": expiry_date
        }
        results.append(result)
        insert_data(results)
        return result
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
