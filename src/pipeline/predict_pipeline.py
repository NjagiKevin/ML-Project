import pandas as pd
import sys
from src.exception import CustomException
from src.utils import load_object # to load our pkl file


# Class for loading a model, preprocessing input data, and making predictions
class PredictPipeline:
    def __init__(self): # initialize the class without any specific attributes
        pass

    def predict(self,features):
        try:
            # Load the trained model and preprocessor
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'

            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            
            # Transform the features
            data_scaled=preprocessor.transform(features)
            
            # Make predictions
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException (e,sys)
        

# Class to structure input data in a way that can be easily converted to a DataFrame for the prediction pipeline
class CustomData:
    def __init__(  self, # initializes a CustomData object with attributes for the model's input features
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    
    def get_data_as_data_frame(self): # This method creates a DataFrame from the attributes of the CustomData object 
        try:
            # Prepare the data in a dictionary form and convert to pandas DataFrame
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict) # Converts the dictionary to a DataFrame and returns it.

        except Exception as e:
            raise CustomException(e, sys)