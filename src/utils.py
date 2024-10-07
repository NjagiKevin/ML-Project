import os
import sys  # for exception handling
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def load_object(file_path):
    """Load a serialized object from a file using dill."""
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)


def save_object(file_path, obj):
    """Save a serialized object to a file using dill."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """Evaluate multiple models using GridSearchCV for hyperparameter tuning."""
    try:
        report = {}

        # Iterate through each model
        for i in range(len(models)):
            model = list(models.values())[i]

            # Hyperparameter tuning
            parameter = param[list(models.keys())[i]]
            gs = GridSearchCV(model, parameter, cv=3)
            gs.fit(X_train, y_train)

            # Set best parameters and fit the model
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Predictions on X_train and X_test
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Compute r2_score
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            # Append results to the report
            report[list(models.keys())[i]] = test_model_score
        
        return report

    except Exception as e:
        raise CustomException(e, sys)
