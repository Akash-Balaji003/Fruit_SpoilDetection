import base64
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

from DB_interface import Get_data, get_fruit_records, insert_data, insert_data_v2, update_expiry_date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can use ["*"] for simplicity but it's less secure
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def classify_fruit_v2(image: Image.Image):
    # Load the trained model
    fruit_model = tf.keras.models.load_model('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/fruit_classifierModel_v2.h5')

    img_size = (128, 128)  # Resize to match model input size
    image = image.resize(img_size)  # Resize image
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
    fruit_names = ['Apple', 'Banana', 'Grapes', 'Guava', 'HogPlum', 'Jackfruit', 'Litchi', 'Mango', 'Orange', 'Papaya']  # Get fruit names from the existing class_map
    return fruit_names[predicted_class_idx[0]]

# Function to classify fruit image
def classify_fruit(image: Image.Image):
    # Load the trained model
    fruit_model = tf.keras.models.load_model('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/fruit_model_v4_1.h5') # Model with oneDNN

    # fruit_model = tf.keras.models.load_model('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_model_v4.h5')

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

def predict_days_to_spoil(fruit_name, temperature, humidity, co2_level):
    lr_algo, ct = joblib.load('/Users/akashbalaji/Desktop/Fruit_SpoilDetection/backend/models/trained_fruit_spoil_model_v3.pkl') # Model with oneDAL
    # Transform the input data
    fruit_encoded = ct.transform([[fruit_name.lower(), temperature, humidity, co2_level]])

    # Make the prediction
    predicted_days = lr_algo.predict(fruit_encoded)

    # Print the number of days to spoil
    print(f"Predicted Days to Spoil: {predicted_days[0]:.2f}")

    return predicted_days[0]

class IoTDataold(BaseModel):
    temperature: float
    humidity: float
    co2_level: float
    fruit_name: str

# Endpoint to get input data without image classification (Temporary)
@app.post("/process_data")
async def process_data(data: List[IoTDataold]):
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
        return result
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def show_info():
    return {"Message":"This API can be accessed by anyone"} 

# Define the request body using Pydantic model
class DataWithBase64Image(BaseModel):
    temperature: float
    humidity: float
    co2_level: float
    image_base64: str

@app.post("/process_data_final_v2")
async def process_data_with_base64_image(data: DataWithBase64Image):
    results = []

    try:
        # Decode the base64 image
        image_data = base64.b64decode(data.image_base64)
        image_pil = Image.open(BytesIO(image_data))

        # Classify the fruit from the image
        fruit_name = classify_fruit(image_pil)

        # Predict days to spoil
        predicted_days = predict_days_to_spoil(fruit_name, data.temperature, data.humidity, data.co2_level)

        today_date = date.today()
        expiry_date = today_date + timedelta(days=predicted_days)

        result = {
            "Item_name": fruit_name,
            "Production_date": today_date,
            "Expiry_date": expiry_date
        }
        results.append(result)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class IoTData(BaseModel):
    temperature: float
    humidity: float
    co2_level: float



# Fianl version_1
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
