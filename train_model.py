import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import (precision_score, recall_score, f1_score, confusion_matrix, classification_report)

# Load dataset
df = pd.read_csv("dataset/diabetes.csv")

# First 5 rows
print("First 5 Rows:")
print(df.head())

# Dataset information
print("\nDataset Info:")
print(df.info())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Statistical summary
print("\nDataset Summary:")
print(df.describe())

# Replace invalid 0 values with column mean

columns_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

for column in columns_to_replace:
    df[column] = df[column].replace(0, df[column].mean())

print("\nAfter Replacing 0 Values:")
print(df.describe())

# Separate features and target

X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Feature Scaling

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)
# Create model

model = RandomForestClassifier(random_state=42)

# Train model

model.fit(X_train, y_train)

# Predictions

y_pred = model.predict(X_test)

# Accuracy

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)

# Precision

precision = precision_score(y_test, y_pred)

# Recall

recall = recall_score(y_test, y_pred)

# F1 Score

f1 = f1_score(y_test, y_pred)

print("\nPrecision:")
print(precision)

print("\nRecall:")
print(recall)

print("\nF1 Score:")
print(f1)

# Confusion Matrix

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Classification Report

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'models/diabetes_model.pkl')

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')

print("Model and Scaler Saved Successfully!")