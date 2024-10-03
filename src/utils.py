import os
import sys # for exception handling
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
import pickle

def load_object(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def save_object(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    


def evaluate_models(X_train,y_train, X_test, y_test,models, param):
    try:
        report={}

        # going through each model
        for i in range(len(list(models))):
            model=list(models.values())[i]
            
            # hyperparameter tuning
            parameter=param[list(models.keys())[i]]
            gs=GridSearchCV(model,parameter,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            
            #model.fit(X_train, y_train)  # train the model

            # predictions on x_train and y_train
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            # computing r2_score
            train_model_score=r2_score(y_train, y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            
            # we keep on appending in this report 
            report[list(models.keys())[i]]=test_model_score

            return report
    
    except Exception as e:
        raise CustomException (e,sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)