import pandas as pd
import streamlit as st
import pandas as pd
import mlflow.sklearn
from sklearn.preprocessing import StandardScaler

# MLflow Tracking URI
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000/"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Weather_Rainfall_SVC")

# Load the production model
production_model_name = "weather-prediction-svc-production"
prod_model_uri = f"models:/{production_model_name}@svc"
loaded_model = mlflow.sklearn.load_model(prod_model_uri)

# Feature names
# feature_names = ['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed']

# Streamlit UI
st.title("Rainfall Prediction App")
st.write("Enter the weather parameters to predict rainfall")

# Input fields
# input_values = []
# for feature in feature_names:
#     value = st.number_input(f"Enter {feature}", value=0.0, format="%.2f")
#     input_values.append(value)

def user_input_features():
    temperature_2m_max = st.number_input("Temperature 2m Max", value=0.0, format="%.2f")
    temperature_2m_min = st.number_input("Temperature 2m Min", value=0.0, format="%.2f")
    apparent_temperature_max = st.number_input("Apparent Temperature Max", value=0.0, format="%.2f")
    apparent_temperature_min = st.number_input("Apparent Temperature Min", value=0.0, format="%.2f")
    daylight_duration = st.number_input("Daylight Duration", value=0.0, format="%.2f")
    sunshine_duration = st.number_input("Sunshine Duration", value=0.0, format="%.2f")
    rain_sum = st.number_input("Rain Sum", value=0.0, format="%.2f")
    wind_speed_10m_max = st.number_input("Wind Speed 10m Max", value=0.0, format="%.2f")
    wind_gusts_10m_max = st.number_input("Wind Gusts 10m Max", value=0.0, format="%.2f")
    wind_direction_10m_dominant = st.number_input("Wind Direction 10m Dominant", value=0.0, format="%.2f")
    shortwave_radiation_sum = st.number_input("Shortwave Radiation Sum", value=0.0, format="%.2f")
    et0_fao_evapotranspiration = st.number_input("ET0 FAO Evapotranspiration", value=0.0, format="%.2f")
    data = {'temperature_2m_max': temperature_2m_max,
                'temperature_2m_min': temperature_2m_min,
                'apparent_temperature_max': apparent_temperature_max,
                'apparent_temperature_min': apparent_temperature_min,
                'daylight_duration': daylight_duration,
                'sunshine_duration': sunshine_duration,
                'rain_sum': rain_sum,
                'wind_speed_10m_max': wind_speed_10m_max,
                'wind_gusts_10m_max': wind_gusts_10m_max,
                'wind_direction_10m_dominant': wind_direction_10m_dominant,
                'shortwave_radiation_sum': shortwave_radiation_sum,
                'et0_fao_evapotranspiration': et0_fao_evapotranspiration,
                }
    features = pd.DataFrame(data, index=[0])
    return features
input_df = user_input_features()

data = pd.read_csv("history_weather_daily_data.csv", index_col = "date")
num_cols = ['temperature_2m_max','temperature_2m_min','apparent_temperature_max','apparent_temperature_min','daylight_duration','sunshine_duration','rain_sum','wind_speed_10m_max','wind_gusts_10m_max','wind_direction_10m_dominant','shortwave_radiation_sum','et0_fao_evapotranspiration']

train_df = data[num_cols]
train_weather_df = train_df.reset_index(drop=True)

weather_raw = train_weather_df.copy()

weather_data = pd.concat([input_df, weather_raw], axis=0)

scaler = StandardScaler()
weather_df = scaler.fit_transform(weather_data)

weather_df = weather_df[:1]

# # Center the button using markdown and CSS
# st.markdown(
#     """
#     <style>
#     .center-button {
#         display: flex;
#         justify-content: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Create a container for centering
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Place the button in the center column
with col3:
    predict_btn = st.button("Predict")

# Predict button

if predict_btn:
    try:
        # Create DataFrame
        input_df = weather_df
        # input_df = pd.DataFrame([input_values], columns=feature_names)

        # Make prediction
        prediction = loaded_model.predict(input_df)
        result = "Drizzling" if prediction[0] == 0 else "No Rain" if prediction[0] == 1 else "Rain"
        # result = "Rainfall" if prediction[0] == 1 else "No Rainfall"

        st.success(f"Prediction: {result}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
