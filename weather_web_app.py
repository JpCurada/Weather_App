import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.write("""

# WAFA: Weather Application For Analysts

This app extract the details and weather's data of your selected location. 

""")
profile = Image.open('profile.jpg')

st.sidebar.image(profile)

st.sidebar.write("""

# Hello, I'm Jeypii!

### This Web-application aims to help users in extracting weather's forecast data from particular areas in the Philippines. 

Contact me\n
Facebook:\nhttps://facebook.com/JeypiiLearns\n
Twitter:\nhttps://twitter.com/JeypiiLearns\n

Visit my GitHub to explore the source code of this project\n
GitHub:\nhttps://github.com/JpCurada\n

I am open for constructive criticisms and your feed back will be highly appreciated.
Feedback: 

""")

choice = st.selectbox('Choose a location:',('Cabanatuan', 'Manila', 'Davao', 'Baguio', 'Albay', 'Batanes','Tarlac','Cebu','Pangasinan'))


def api_call():
    plt.style.use(['science', 'notebook', 'grid'])
    city = choice
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q":city,"days":"10"}

    headers = {
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        "X-RapidAPI-Key": "e575b5a70emsh763f0069abf73bfp17b405jsn6bee8d65a5d8"
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)

    return response

def location_weather_details(df_details):
    date = response['forecast']['forecastday'][0]['date']
    location = response['location']['name']
    country = response['location']['country']
    longitude = response['location']['lon']
    latitude = response['location']['lat']
    sunrise = response['forecast']['forecastday'][0]['astro']['sunrise']
    sunset = response['forecast']['forecastday'][0]['astro']['sunset']
    moon_phase = response['forecast']['forecastday'][0]['astro']['moon_phase']
    
            
    df_details = df_details.append({'Date': date,
                                    'Location':location,
                                    'Country':country,
                                    'Longitude': longitude,
                                    'Latitude': latitude,
                                    'Sunrise':sunrise,
                                    'Sunset':sunset,
                                    'Moon Phase':moon_phase},ignore_index=True)
    
    return df_details

def get_day_forecast(df):
    time_of_the_day = response['forecast']['forecastday'][0]['hour']
    for idx, hour in enumerate(time_of_the_day):
        time = time_of_the_day[idx]['time'].split(' ')
        time = datetime.strptime(time[1],'%H:%M').strftime('%I:%M %p')
        temperature_c = time_of_the_day[idx]['temp_c']
        heat_index_c = time_of_the_day[idx]['heatindex_c']
        humidity = time_of_the_day[idx]['humidity']
        wind_kph = time_of_the_day[idx]['wind_kph']

        df = df.append({'Time': time, 
                        'Temperature[°C]':temperature_c,
                        'Heat Index[°C]':heat_index_c,
                        'Humidity[%]':humidity,
                        'Wind[km/h]':wind_kph}, ignore_index=True)

    return df

def graph_forecast(df_details):
    # Temperature
    x = np.array(['12 AM','1 AM','2 AM','3 AM','4 AM','5 AM','6 AM','7 AM','8 AM','9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM','5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM'])
    y = df['Temperature[°C]'].values
    # Heat Index
    x2 = x
    y2 = df['Heat Index[°C]'].values
    plt.figure(figsize=(35,10))
    plt.plot(x,y, 'o--', label='Temperature',color='orange', lw=2, ms=15)
    plt.plot(x2,y2,'o--', label='Heat Index',color='gray', lw=2, ms=15)
    plt.xlabel('Time',color='brown', fontsize=25)
    plt.ylabel('Degree Celsius [°C]',color='brown', fontsize=25)
    plt.legend(loc='upper right', fontsize=30, ncol=2)
    plt.title(f"{df_details['Location'].values[0]}, {df_details['Country'].values[0]} Today's Weather ({df_details['Date'].values[0]})", color='brown', fontsize=50)



    fig_png = plt.savefig(f"{df_details['Location'].values[0]}, {df_details['Country'].values[0]} Graph ({df_details['Date'].values[0]}).png")
    return fig_png

response = api_call()
df_details = pd.DataFrame(columns=['Date', 'Location', 'Country', 'Longitude','Latitude','Sunrise','Sunset','Moon Phase'])
df_details = location_weather_details(df_details)
df = pd.DataFrame(columns=['Time','Temperature[°C]','Heat Index[°C]','Humidity[%]','Wind[km/h]'])
df = get_day_forecast(df)
graph = graph_forecast(df_details)


st.header('Location Details')
st.dataframe(df_details)
st.write(f"""

### {df_details['Location'].values[0]}, {df_details['Country'].values[0]} Today's Weather Forecast

""")
st.dataframe(df)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(df)
details = convert_df(df_details)

st.download_button(
     label="Download data as CSV",
     data=details+csv,
     file_name='WeatherData.csv',
     mime='text/csv',
 )


st.write(f"""

##### {df_details['Location'].values[0]}, {df_details['Country'].values[0]}: Temperature and Heat Index

""")
image = Image.open(f"{df_details['Location'].values[0]}, {df_details['Country'].values[0]} Graph ({df_details['Date'].values[0]}).png")

st.image(image, caption='Temperature and Heat Index Relationship')

with open(f"{df_details['Location'].values[0]}, {df_details['Country'].values[0]} Graph ({df_details['Date'].values[0]}).png", "rb") as file:
     btn = st.download_button(
             label="Download image",
             data=file,
             file_name="TempAndHeatInd.png",
             mime="image/png"
           )
