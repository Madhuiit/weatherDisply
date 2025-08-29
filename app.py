
from flask import Flask, render_template, request, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()  # Secure secret key for session/flash

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'f2d90162b16747e83ef26437df82e464')  # Replace with your API key or use .env
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash('Please enter a city name!')
            return render_template('index.html', weather_data=weather_data)
        else:
            # Make API request
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()  # Raise exception for bad status codes
                data = response.json()
                
                if data.get('cod') != 200:
                    flash(f"Error: {data.get('message', 'City not found')}")
                    return render_template('index.html', weather_data=weather_data)
                else:
                    # Extract relevant weather data
                    weather_data = {
                        'city': data['name'],
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'].capitalize(),
                        'humidity': data['main']['humidity'],
                        'icon': data['weather'][0]['icon']
                    }
            except requests.RequestException as e:
                flash(f"Error fetching weather data: {str(e)}")
                return render_template('index.html', weather_data=weather_data)
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
  
                            

 




