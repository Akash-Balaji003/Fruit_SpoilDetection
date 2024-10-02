"""

This model has used oneDAL

"""

# Importing the Libraries
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearnex.linear_model import LinearRegression
from sklearnex import patch_sklearn
patch_sklearn()

# Load the dataset
dataset = pd.read_csv('backend/datasets/augmented_fruit_data_250.csv')

# Separate features and target
X = dataset.iloc[:, :4].values
y = dataset.iloc[:, -1].values

# Apply One-Hot Encoding to the fruit column
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = ct.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr_algo = LinearRegression()
lr_algo.fit(X, y)
coef = lr_algo.coef_
intercept = lr_algo.intercept_

# Predict on the test set using the oneDAL optimized LinearRegression
y_pred = lr_algo.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
accuracy = lr_algo.score(X_test, y_test)
print(f'Mean Squared Error: {mse}')
print(f'R-squared Score: {r2}')
print(f'Accuracy: {accuracy}')

print("Saving model...")
# Save the trained model to a file
joblib.dump((lr_algo, ct), 'backend/models/trained_fruit_spoil_model_v3.pkl')
print("Saved the model...")

# Visualizing Predicted vs Actual values with different colors
plt.scatter(range(len(y_test)), y_test, color='red', label='Actual')
plt.scatter(range(len(y_pred)), y_pred, color='blue', label='Predicted')
plt.title('Predicted vs Actual Days to Spoil')
plt.xlabel('Sample Index')
plt.ylabel('Days to Spoil')
plt.legend()
plt.show()
