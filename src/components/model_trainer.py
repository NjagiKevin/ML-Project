import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn import preprocessing
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.pipeline import predict_pipeline
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig():
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self, train_array,test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test,y_test = (
                train_array[:,:-1], # everything minus the last column, store in X_train
                train_array[:,-1], # last data as y_train value
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGB Classifier": XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "KNN Classifier": KNeighborsRegressor(),
                "AdaBoost Classifier": AdaBoostRegressor(),
                "Linear Regression": LinearRegression(),
            }

            model_report:dict=evaluate_models(X_train=X_train,
                                             y_train=y_train,
                                             X_test=X_test,
                                             y_test=y_test,
                                             models=models)

            # getting the best model score from dictionary
            best_model_score=max(sorted(model_report.values()))

            # getting best model name from the dictionary
            best_model_name=list(model_report.keys())[ # model.keys is converted to a list
                list(model_report.values()).index(best_model_score) # a nested list in respect to the report values
            ]
            best_model=models[best_model_name]


            if best_model_score<0.6:
                raise CustomException("No best model found")
    
            logging.info("Best found model on both train and test data is: %s",best_model_name)

            # saving our best model as model.pkl
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square=r2_score(y_test, predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)