import os
import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
import xgboost as xgb
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff

class DelayModel:

    def __init__(self):

        self._model = None
        self.target_column = None
        self.model_dir = os.path.join(current_dir, "models/")
        self.model_path = os.path.join(self.model_dir, "model.json")

        os.makedirs(self.model_dir, exist_ok=True)
        
        self.feature_cols = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air",
        ]

    def load_model(
        self,
    )-> None:
        """
        Load the model from directory.

        """
        if os.path.isfile(self.model_path):
            self._model = xgb.XGBClassifier()
            self._model.load_model(self.model_path)
        else:
            raise ValueError(f"No trained model found at {self.model_path}."
                + " Please call the 'fit' method first."
            )

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        # Feature Engineering
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix='MES')], 
            axis=1)

        # Make sure all top_10_features are present in the dataframe
        for col in self.feature_cols:
            if col not in features.columns:
                features[col] = 0
        
        features = features[self.feature_cols]

        self.target_column = target_column
        
        if target_column:
            data['min_diff'] = data.apply(get_min_diff, axis = 1)
            threshold_in_minutes = 15
            data[target_column] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)
            target = data[target_column]
            target = pd.DataFrame(data[target_column], columns=[target_column])
            return features, target
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        target = target[self.target_column]
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0/n_y1

        features = features[self.feature_cols]

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.fit(features, target)
        self._model.save_model(self.model_path)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        features = features[self.feature_cols]
        if self._model:
            y_preds = self._model.predict(features)
            return y_preds.tolist()
        else:
            self.load_model()
            y_preds = self._model.predict(features)
            return y_preds.tolist()
