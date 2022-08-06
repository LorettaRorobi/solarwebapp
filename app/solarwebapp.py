import streamlit as st
import json
import requests
import numpy as np
import pandas as pd
from app.solar_irradiation import Get_Radiation

# this is the main function in which we define our webpage
def main():
    proposed_land_area = 190354330.7 #1% of the total proposed land area of Abia, Enugu, Anambra, and Ebonyi combined
    efficiency_of_solar_mono_pv_module = 0.28 # 28%
    efficiency_of_solar_poly_pv_module = 0.198 # 19.8% 
    area_of_the_residential_panels = 2535 #65 by 39 inches
    area_of_commercial_panels = 3042 #78 by 39 inches
    conversion_factor = 1000000000 # to express energy in GigaWatt       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:green;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Regional Solar Prediction App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    st.sidebar.title('PV Design Features')
    option_efficiency = st.sidebar.selectbox('Select type of PV Module based on Efficiency', ('Mono_Crystalline_0.28', 'Poly_Crystalline_0.198'))
    option_size = st.sidebar.selectbox('Select type of PV Module based on Size', ('Residential_PV', 'Commercial_PV'))
    st.sidebar.title('Model features')   
    Temperature = st.sidebar.number_input("Temperature")
    CloudOpacity = st.sidebar.number_input("CloudOpacity")
    DHI = st.sidebar.number_input("DHI")
    DNI = st.sidebar.number_input("DNI")
    Precipitation = st.sidebar.number_input("Precipitation")
    Humidity = st.sidebar.number_input("Humidity")
    Pressure = st.sidebar.number_input("Pressure")
    WindDirection = st.sidebar.number_input("WindDirection")
    WindSpeed = st.sidebar.number_input("WindSpeed")
    Month = st.sidebar.number_input("Month")
    Day = st.sidebar.number_input("Day")

    data = {
        'Temperature': Temperature,  
        'CloudOpacity': CloudOpacity, 
        'DHI': DHI,
        'DNI': DNI,
        'Precipitation': Precipitation,
        'Humidity': Humidity,
        'Pressure': Pressure,
        'WindDirection': WindDirection,
        'WindSpeed': WindSpeed,
        'Month': Month,
        'Day': Day
        }

      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.sidebar.button("Predict"): 

            # Converting Features into DataFrame

        features_df  = pd.DataFrame([data]).astype({'Temperature': 'float',  
                                                    'CloudOpacity': 'float', 
                                                    'DHI': 'float',
                                                    'DNI': 'float',
                                                    'Precipitation': 'float',
                                                    'Humidity': 'float',
                                                    'Pressure': 'float',
                                                    'WindDirection': 'float',
                                                    'WindSpeed': 'float',
                                                    'Month': 'int64',
                                                    'Day': 'int64'
                                                    })

        st.markdown('##')
        st.table(features_df)

        features_df.fillna(0, inplace = True)
        features_df = list(features_df.iloc[0])
        if any(features_df) == 0:
            st.write("imput missing values")
        else:
            result = Solar_Estimator(features_df)
            st.success('Solar Irradiation {}'.format(result))
            #print(result)
        st.markdown('##')

        if option_efficiency == str("Mono_Crystalline_0.28") and option_size == str("Residential_PV"):
            Output_Energy = round(result * efficiency_of_solar_mono_pv_module * area_of_the_residential_panels, 2)
            Number_of_panels = round(proposed_land_area / area_of_the_residential_panels)
            Total_Energy = round((Output_Energy * Number_of_panels)/conversion_factor, 2)
            st.success('Total Estimated Energy(in GigaWatts) Generated on the selected date: {}'.format(Total_Energy))
            st.success("Number of solar residential PV modules required {}".format(Number_of_panels))

        elif option_efficiency == str("Mono_Crystalline_0.28") and option_size == str("Commercial_PV"):
            Output_Energy = round(result * efficiency_of_solar_mono_pv_module * area_of_commercial_panels, 2)
            Number_of_panels = round(proposed_land_area / area_of_commercial_panels)
            Total_Energy = round((Output_Energy * Number_of_panels)/conversion_factor, 2)
            st.success('Total Estimated Energy(in GigaWatts) Generated on the selected date: {}'.format(Total_Energy))
            st.success("Number of solar commercial PV modules required {}".format(Number_of_panels))

        elif option_efficiency == str("Poly_Crystalline_0.198") and option_size == str("Residential_PV"):
            Output_Energy = round(result * efficiency_of_solar_poly_pv_module * area_of_the_residential_panels, 2)
            Number_of_panels = round(proposed_land_area / area_of_the_residential_panels)
            Total_Energy = round((Output_Energy * Number_of_panels)/conversion_factor, 2)
            st.success('Total Estimated Energy(in GigaWatts) Generated on the selected date: {}'.format(Total_Energy))
            st.success('Number of solar residential PV modules required {}'.format(Number_of_panels))

        else:
            Output_Energy = round(result * efficiency_of_solar_poly_pv_module * area_of_commercial_panels, 2)
            Number_of_panels = round(proposed_land_area / area_of_commercial_panels)
            Total_Energy = round((Output_Energy * Number_of_panels)/conversion_factor, 2)
            st.success('Total Estimated Energy(in GigaWatts) Generated on the selected date: {}'.format(Total_Energy))
            st.success('Number of solar commercial PV modules required  {}'.format(Number_of_panels)) 

def Solar_Estimator(features_df):
        """
            Get inputs from users and return estimated solar radiation. 
        """
        try:
            results = Get_Radiation(features_df)

        except:

            return None
        
        return round(results, 2)