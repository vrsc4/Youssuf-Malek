from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)


WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')

def get_coordinates(city):
    
    geolocator = Nominatim(user_agent="global_weather_tracker")
    try:
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def get_weather_data(lat, lon):
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Weather API error: {e}")
        return None

def analyze_weather_prediction(weather_data):
    
    if not weather_data:
        return "Unable to retrieve weather data."
    
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    prediction = f"Current conditions: {temp}°C with {description}. "
    
    if temp < 10:
        prediction += "Bundle up, it's quite cold! "
    elif temp < 20:
        prediction += "Mild temperature, a light jacket might be good. "
    else:
        prediction += "Warm weather today! "
    
    if humidity > 80:
        prediction += "High humidity expected. "
    
    if wind_speed > 5:
        prediction += "Windy conditions detected. "
    
    return prediction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_weather():
    city = request.form.get('city')
    
    
    coords = get_coordinates(city)
    if not coords:
        return jsonify({'error': 'Could not find coordinates for the city'}), 400
    
    
    weather_data = get_weather_data(coords[0], coords[1])
    if not weather_data:
        return jsonify({'error': 'Could not retrieve weather data'}), 500
    
    
    prediction = analyze_weather_prediction(weather_data)
    
    return jsonify({
        'city': city,
        'prediction': prediction,
        'temp': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description']
    })

if __name__ == '__main__':
    app.run(debug=True)
