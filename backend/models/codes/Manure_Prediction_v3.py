import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings

# Suppress warnings from sklearn
warnings.filterwarnings("ignore", category=UserWarning)

# Load manure dataset (Manure prediction dataset)
manure_data = pd.read_csv('backend/datasets/synthetic_fruit_decomposition_data_1000.csv')  # Using the synthetic dataset

# Prepare features and target for the model
X = manure_data[['Fruit Waste (kg)', 'C:N Ratio', 'Time to Manure (weeks)']]
y = manure_data['Finished Manure (kg)']

# Create and train the linear regression model
manure_model = LinearRegression()
manure_model.fit(X, y)

# Training is done, no further actions.
print("Model training complete.")

print("Saving model...")
# Save the trained model to a file
joblib.dump((manure_model), 'backend/models/Manure_v4.pkl')
print("Saved the model...")