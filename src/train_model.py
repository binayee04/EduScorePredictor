import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the original student performance dataset
df = pd.read_csv("../data/raw/StudentsPerformance.csv")

# Create a new column called "average_score" by taking the mean of math, reading, and writing scores
df["average_score"] = df[["math score", "reading score", "writing score"]].mean(axis=1)

# Define X (features) and y (target/output). We drop "average_score" from X because it's what we're trying to predict
X = df.drop(columns=["average_score"])
y = df["average_score"]

# Convert categorical data into numerical format using one-hot encoding
X_encoded = pd.get_dummies(X)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model with 100 trees
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file so we can use it later in our app
model_path = "model.pkl"
joblib.dump(model, model_path)

# Let us know the model was saved successfully
print("✅ Model trained and saved to:", model_path)
