import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object



# specifies the path where the preprocessor (pipeline for transforming data) will be saved (preprocessor.pkl)
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")


# This class is responsible for transforming the data, i.e., handling missing values, scaling numerical columns, and one-hot encoding categorical columns
class DataTransformation:
    def __init__(self): # The constructor initializes an instance of DataTransformationConfig
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self): #creates all pkl files responsible for standard scaling and OHE
        '''
        This fxn is will be used for data transformation
        '''
        
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # numerical pipeline->missing values & std scaler
            numerical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            # categorical  pipeline->missing values, std scaling & OHE

            categorical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore",sparse_output=True)), # Using sparse matrix output
                    ("scaler",StandardScaler(with_mean=False)) ## Set with_mean=False to avoid dense conversion of sparse matrix
                ]
            )

            logging.info(f"Numerical columns: {numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")
            
            #comibining both numerical & categorical pipleline
            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_columns),
                    ("categorical_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test completed")

            logging.info("Obtaining preproccing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns=["writing_score","rading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]


            logging.info(
                f"Applying preprocessing object on traing dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[ # np.c_ combines two arrays as columns
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            
            test_arr=np.c_[ 
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object")
            
            #saving the pkl file
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
            