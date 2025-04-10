import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
import os
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from src.utils import save_object
from src.components.data_ingestion import DataIngestion



@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join('artifacts', 'preprocessor.joblib')
    transformed_train_path: str = os.path.join('artifacts', 'transformed_train.csv')
    transformed_test_path: str = os.path.join('artifacts', 'transformed_test.csv')

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        '''
        Creates and returns a data transformer object that handles:
        1. Numerical features:
           - Imputes missing values with median
           - Scales features using StandardScaler
        2. Categorical features:
           - Imputes missing values with most frequent
           - Applies one-hot encoding
        Returns:
            ColumnTransformer: A configured preprocessing pipeline
        '''
        try:
            categorical_features = ['gender', 'race/ethnicity', 'parental level of education', 'lunch','test preparation course']  
            numerical_features = ['reading score', 'writing score'] 

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_features),
                    ('cat_pipeline', cat_pipeline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Starting data transformation")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data")

            preprocessing_obj = self.get_data_transformer()

            input_feature_train_df = train_df.drop(columns=['math score'], axis=1)
            target_feature_train_df = train_df['math score']
            input_feature_test_df = test_df.drop(columns=['math score'], axis=1)
            target_feature_test_df = test_df['math score']

            logging.info("Applying preprocessing on train and test data")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            os.makedirs(os.path.dirname(self.transformation_config.transformed_train_path), exist_ok=True)
            pd.DataFrame(train_arr).to_csv(self.transformation_config.transformed_train_path, index=False)
            pd.DataFrame(test_arr).to_csv(self.transformation_config.transformed_test_path, index=False)

            save_object(file_path=self.transformation_config.preprocessor_path,obj=preprocessing_obj)

            logging.info("Data transformation completed")
            return (
                self.transformation_config.transformed_train_path,
                self.transformation_config.transformed_test_path,
                self.transformation_config.preprocessor_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e

