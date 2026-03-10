# Heart Disease Risk Predictor

A Machine Learning web application that predicts the probability of cardiovascular disease using patient health data. The system uses a Logistic Regression model trained on a cardiovascular dataset and exposes predictions through a FastAPI backend, with a Streamlit frontend dashboard.

## Live Demo

Streamlit App:
https://iamarnav23-heart-risk-predictor.streamlit.app/

FastAPI Backend:
https://heart-risk-predictor-7b16.onrender.com

## Technical Results

• Dataset size: ~70,000 patient records
• Number of features used: 12
• Train/Test split: 80 / 20
• Model performance:
• Accuracy: ~0.73
• ROC-AUC Score: ~0.79
• Precision: ~0.72
• Recall: ~0.74

## What This Project Demonstrates

• This project focuses on building a complete ML application pipeline, including:
• Machine Learning model development
• Model serialization using pickle
• API development using FastAPI
• Frontend development using Streamlit
• Cloud deployment using Render
• Integration between UI → API → ML model

## Project Disclaimer

This project is not intended to provide medical diagnosis or real-world healthcare advice. The dataset used for training is a public cardiovascular dataset that was collected years ago and may not reflect current medical practices, lifestyle changes, or modern treatment advancements. Because of this, predictions from the model should not be interpreted as real medical risk assessments.


