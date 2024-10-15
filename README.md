# Fruit Spoil Detection System

This project focuses on predicting the spoilage of fruits using IoT sensor data to support food sustainability. By leveraging environmental data like temperature, humidity, and CO₂ levels, it provides a predictive model for fruit spoilage in storage facilities. This solution is crucial for reducing food wastage and ensuring optimal storage conditions.

## Overview

The Fruit Spoil Detection system integrates hardware sensors with a software stack to gather, process, and analyze data. The ESP8266 device collect temperature, humidity, and CO₂ levels from the storage environment, and images of fruits are processed using machine learning models. The FastAPI backend handles data ingestion and analysis, while the React frontend provides a dashboard for visualizing spoilage predictions.

## Features

- **IoT Data Collection**: Uses ESP8266 to capture environmental parameters like temperature, humidity, and CO₂ levels via the DHT11 and MQ135 sensors.
- **FastAPI Backend**: Provides endpoints to process data, store it in a MySQL database, and apply machine learning models.
- **React Frontend**: Displays sensor readings, spoilage predictions, and real-time alerts.
- **Database Integration**: Uses MySQL for storage of sensor readings and prediction data.
- **Machine Learning Model**: Linear Regression models to predict expiry dates of the fruits and predicting the amount of manure the spoiled food can produce.

## Project Structure

```plaintext
Fruit_SpoilDetection/
│
├── backend/               # FastAPI backend
│   ├── app.py             # Main FastAPI app
│   ├── models/            # Machine learning models
│   ├── routes/            # API route definitions
│   ├── services/          # Image processing and sensor data handling
│   └── database/          # MySQL connection and ORM setup
│
├── frontend/              # React frontend
│   ├── src/
│   ├── public/
│   └── package.json       # Project dependencies
│
└── docs/                  # Project documentation and guides
```

## Installation

### Prerequisites

- **Hardware**: ESP8266, DHT11, MQ135 sensors
- **Software**:
  - Python 3.9+
  - Node.js
  - MySQL

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Akash-Balaji003/Fruit_SpoilDetection.git
   cd Fruit_SpoilDetection
   ```

2. **Backend Setup**:
   - Navigate to the backend folder:
     ```bash
     cd backend
     ```
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure your MySQL database in `database/config.py` with the appropriate credentials.

3. **Frontend Setup**:
   - Navigate to the frontend folder:
     ```bash
     cd ../frontend
     ```
   - Install the required dependencies:
     ```bash
     npm install
     ```

## Usage

1. **Run the Backend**:
   - Start the FastAPI backend server:
     ```bash
     uvicorn app:app --reload
     ```

2. **Run the Frontend**:
   - Start the React application:
     ```bash
     npm start
     ```

3. **Sensor Data Input**:
   - Use ESP8266 to send data to the FastAPI backend using the provided API endpoints. The system will process the data and store it in MySQL.

4. **View Data**:
   - Access the React dashboard at `http://localhost:3000` to visualize real-time sensor data and predictions for fruit spoilage.

## API Endpoints

### Sensor Data Ingestion
- **POST** `/api/sensors/` - Accepts temperature, humidity, CO₂ level.

### Spoilage Prediction
- **GET** `/api/predictions/` - Returns spoilage predictions based on the collected data.

### Database Operations
- **GET** `/api/data/` - Fetches stored sensor data.
- **POST** `/api/data/` - Stores new sensor data in MySQL.

## Machine Learning Models
The project includes two machine learning models:

**Expiry Date Prediction Model**: A predictive model that uses environmental factors like temperature, humidity, and CO₂ levels to estimate the expiry date of stored fruits. This helps in managing fruit storage effectively and preventing spoilage.

**Manure Prediction Model**: A predictive model designed to forecast manure production or usage, which helps optimize agricultural practices related to soil fertilization. This model can enhance decision-making in agriculture by estimating how much manure should be used based on various factors.

## Future Improvements

- **Improved Sensor Integration**: Add more sensors like gas sensors to monitor other volatile compounds released during spoilage.
- **Enhanced Machine Learning Models**: Improve the accuracy and performance of the spoilage prediction model using larger datasets and more advanced neural networks.
- **Alert System**: Implement an alert mechanism to notify users of imminent spoilage via SMS or email.

## Contributions

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Open a pull request with a detailed description.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Let me know if you'd like further adjustments!
