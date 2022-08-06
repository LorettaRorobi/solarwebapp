import joblib
import json
import numpy as np
import pandas as pd

def Get_Radiation(raw_data):
    """
    Inputs: Temperature, CloudOpacity, DHI, DNI, Precipitation, Humidity, Pressure, WindDirection, WindSpeed, Month, Day
    Output: Radiation
    """
    """
    data = np.array(input_data).reshape(1, 124)
    file_name = 'models/model_rfr_nig_v1.pkl'
    loaded_model = joblib.load(open(file_name, 'rb'))

    predicted_price = loaded_model.predict(data)[0]
    #input_data = Transform_Input(raw_data)
    input_data = list(raw_data.values())
    """

    data = np.array(raw_data).reshape(1, 11)
    file_name = 'models/model_rfr.pkl'
    loaded_model = joblib.load(open(file_name, 'rb'))

    predicted_result = loaded_model.predict(data)[0]

    return predicted_result