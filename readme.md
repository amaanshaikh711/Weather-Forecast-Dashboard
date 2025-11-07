🌤️ India Weather Dashboard

A modern and fully responsive real-time weather visualization dashboard built with Python, Dash, and Plotly.
It fetches live weather data from the OpenWeatherMap API and presents it in an elegant one-page layout — complete with dynamic charts, blur effects, and adaptive backgrounds that change with the weather and time of day.

🚀 Features

🌍 Real-Time Weather Data: Fetches live data for major Indian cities using the OpenWeatherMap API.

📊 Interactive Charts: Visualizes temperature trends and rainfall probability with smooth Plotly graphs.

💨 Weather Metrics Cards: Displays temperature, humidity, wind speed, pressure, and visibility in clean, uniform cards.

🎚️ Rain Chart Toggle: Option to show or hide the 7-day rain probability graph to keep the interface clean.

🧠 Tech Stack

Python

Dash & Plotly

Dash Bootstrap Components

Pandas

OpenWeatherMap API

⚙️ Setup Instructions

Clone the repository:

git clone https://github.com/<your-username>/india-weather-dashboard.git
cd india-weather-dashboard


Install dependencies:

pip install dash dash-bootstrap-components plotly requests pandas pytz


Get your free API key from OpenWeatherMap
 and replace it inside the script:

API_KEY = "your_api_key_here"


Run the app:

python weather_dashboard.py


Open your browser at:

http://127.0.0.1:8050/

📸 Preview

A visually clean, real-time weather dashboard showing:

Live temperature chart for 24 hours

Dynamic background changing with weather

Neatly aligned weather metric cards

(You can include screenshots or a GIF demo here)

💡 Future Improvements

Add search support for any global city

Include air quality data (AQI)

Create a mobile app version using Streamlit or Flutter

🧑‍💻 Developer

Amaan Shaikh
Computer Science Student | AI & ML Enthusiast
📍 University of Mumbai
