from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd
from app.schema import Score
from src.pipeline import predict_pipeline

from sklearn.preprocessing import StandardScaler

app=FastAPI()


# Home route to check if API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Score Prediction API!"}


# Prediction route
@app.post("/predict")
def predict(data: Score):
    try:
        # Convert input data to a dataframe using CustomData class
        custom_data = predict_pipeline.CustomData(
            gender=data.gender,
            race_ethnicity=data.race_ethnicity,
            parental_level_of_education=data.parental_level_of_education,
            lunch=data.lunch,
            test_preparation_course=data.test_preparation_course,
            reading_score=data.reading_score,
            writing_score=data.writing_score,
        )
        # Convert the custom data to a pandas DataFrame
        input_df = custom_data.get_data_as_data_frame()

        # Initialize the PredictPipeline and make predictions
        pipeline = predict_pipeline.PredictPipeline()  
        prediction = pipeline.predict(input_df)

        # Return the prediction as JSON
        return {"prediction": prediction.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

