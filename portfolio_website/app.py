from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects/password_generator')
def password_generator():
    return send_from_directory('projects/password_generator', 'index.html')

@app.route('/projects/freefall_simulator')
def freefall_simulator():
    return send_from_directory('projects/freefall_simulator', 'index.html')

@app.route('/projects/calculus_calculator')
def calculus_calculator():
    return send_from_directory('projects/calculus_calculator', 'index.html')

@app.route('/projects/global_weather_tracker')
def global_weather_tracker():
    return send_from_directory('projects/global_weather_tracker', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
