import os
import sys
from src.exception import CustomException
from src.logger import logging
import joblib

def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)