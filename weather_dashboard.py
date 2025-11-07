import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests
import pandas as pd
from datetime import datetime
import pytz

# API Configuration
API_KEY = "836d5a8d1625aea62b68110b92c3a651"
BASE_URL = "http://api.openweathermap.org/data/2.5/"

# Major Indian Cities with Coordinates
INDIAN_CITIES = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "tz": "Asia/Kolkata"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "tz": "Asia/Kolkata"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "tz": "Asia/Kolkata"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "tz": "Asia/Kolkata"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "tz": "Asia/Kolkata"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "tz": "Asia/Kolkata"},
    "Chittoor": {"lat": 13.2172, "lon": 79.1003, "tz": "Asia/Kolkata"}
}

# Color Scheme
COLORS = {
    'bg': '#0a0e14',
    'card': 'rgba(20, 25, 35, 0.9)',
    'accent': '#2d3748',
    'text': '#e2e8f0',
    'highlight': '#4299e1',
    'success': '#48bb78',
    'warning': '#ed8936',
    'danger': '#f56565'
}

def get_weather(lat, lon):
    """Fetch current weather data from OpenWeatherMap API"""
    try:
        url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': round(data['main']['pressure'], 2),
                'wind_speed': round(data['wind']['speed'] * 3.6, 2),
                'visibility': round(data.get('visibility', 10000) / 1000, 1),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'clouds': data['clouds']['all']
            }
        return None
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None

def get_forecast(lat, lon):
    """Fetch 5-day forecast data from OpenWeatherMap API"""
    try:
        url = f"{BASE_URL}forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            forecasts = []
            for item in data['list'][:40]:
                forecasts.append({
                    'dt': datetime.fromtimestamp(item['dt']),
                    'temp': round(item['main']['temp'], 1),
                    'humidity': item['main']['humidity'],
                    'wind': round(item['wind']['speed'] * 3.6, 1),
                    'rain': round(item.get('pop', 0) * 100, 0),
                    'desc': item['weather'][0]['description']
                })
            return forecasts
        return []
    except Exception as e:
        print(f"Forecast API Error: {e}")
        return []

def create_temp_chart(forecasts):
    """Create 24-hour temperature line chart with proper time labels"""
    if not forecasts:
        return go.Figure()
    
    df = pd.DataFrame(forecasts[:24])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['dt'],
        y=df['temp'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#4299e1', width=4),
        marker=dict(size=8, color='#4299e1'),
        fill='tozeroy',
        fillcolor='rgba(66, 153, 225, 0.15)',
        hovertemplate='%{y}°C<br>%{x|%I:%M %p}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='24-Hour Temperature Forecast',
            font=dict(size=18, color=COLORS['text'], family='Arial'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], size=12, family='Arial'),
        height=320,
        margin=dict(l=50, r=30, t=50, b=50),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            color=COLORS['text'],
            tickformat='%I:%M %p',
            dtick=3600000*4,
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)', 
            color=COLORS['text'],
            title=dict(text='Temperature (°C)', font=dict(size=12)),
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        showlegend=False
    )
    return fig

def create_weekly_overview(forecasts):
    """Create weekly weather overview cards"""
    if not forecasts:
        return []
    
    daily_forecasts = {}
    for f in forecasts:
        day_key = f['dt'].strftime('%Y-%m-%d')
        if day_key not in daily_forecasts:
            daily_forecasts[day_key] = f
    
    days = list(daily_forecasts.values())[:7]
    
    cards = []
    for f in days:
        icon = '☁️' if 'cloud' in f['desc'].lower() else '☀️' if 'clear' in f['desc'].lower() else '🌧️' if 'rain' in f['desc'].lower() else '🌫️'
        
        cards.append(
            html.Div([
                html.Div(f['dt'].strftime('%a'), 
                        style={'fontSize': '15px', 'marginBottom': '12px', 'fontWeight': '600', 
                               'color': COLORS['text'], 'height': '20px'}),
                html.Div(icon,
                        style={'fontSize': '28px', 'marginBottom': '10px', 'height': '35px', 
                               'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div(f"{f['temp']}°",
                        style={'fontSize': '17px', 'fontWeight': 'bold', 'color': COLORS['highlight'],
                               'height': '25px'})
            ], style={
                'textAlign': 'center',
                'padding': '15px 10px',
                'backgroundColor': 'rgba(45, 55, 72, 0.7)',
                'borderRadius': '10px',
                'minWidth': '75px',
                'flex': '1',
                'margin': '0 3px',
                'border': '1px solid rgba(255,255,255,0.1)',
                'height': '100px',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'space-between'
            })
        )
    
    return html.Div(cards, style={
        'display': 'flex', 
        'justifyContent': 'space-between',
        'gap': '8px',
        'alignItems': 'center',
        'overflow': 'hidden',
        'padding': '0',
        'height': '100px'
    })

def create_metric_card(icon, label, value, unit):
    """Create weather metric display card"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(icon, style={'fontSize': '28px', 'marginRight': '12px', 'opacity': '0.9'}),
                html.Div([
                    html.Div(label, style={'fontSize': '12px', 'opacity': '0.7', 'marginBottom': '4px', 'fontWeight': '500'}),
                    html.Div([
                        html.Span(str(value), style={'fontSize': '22px', 'fontWeight': 'bold', 'color': COLORS['text']}),
                        html.Span(unit, style={'fontSize': '13px', 'marginLeft': '4px', 'opacity': '0.8'})
                    ])
                ])
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'padding': '18px'})
    ], style={
        'backgroundColor': 'rgba(20, 25, 35, 0.8)',
        'border': '1px solid rgba(255,255,255,0.1)',
        'borderRadius': '12px',
        'height': '100%'
    })

def get_background_style(weather_desc, current_hour):
    """Generate dynamic background with dark theme and subtle weather colors"""
    weather_desc_lower = weather_desc.lower()
    
    # Always dark base with subtle weather accents
    if 'rain' in weather_desc_lower:
        gradient = "linear-gradient(135deg, #0a0e14 0%, #1a1f2e 30%, #2d3748 70%, #4a5568 100%)"
    elif 'cloud' in weather_desc_lower:
        gradient = "linear-gradient(135deg, #0a0e14 0%, #1e293b 40%, #374151 80%, #4b5563 100%)"
    elif 'clear' in weather_desc_lower:
        gradient = "linear-gradient(135deg, #0a0e14 0%, #1e293b 30%, #1e40af 70%, #3b82f6 100%)"
    elif 'snow' in weather_desc_lower:
        gradient = "linear-gradient(135deg, #0a0e14 0%, #1e293b 40%, #374151 80%, #6b7280 100%)"
    else:
        gradient = "linear-gradient(135deg, #0a0e14 0%, #1a1f2e 50%, #2d3748 100%)"
    
    return {
        'background': gradient,
        'minHeight': '100vh',
        'height': '100vh',
        'overflow': 'auto',
        'padding': '20px',
        'color': COLORS['text'],
        'position': 'relative',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "India Weather Dashboard"

# Custom CSS for enhanced styling with dropdown on top
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(66, 153, 225, 0.6);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(66, 153, 225, 0.8);
            }
            
            /* Firefox Scrollbar */
            * {
                scrollbar-width: thin;
                scrollbar-color: rgba(66, 153, 225, 0.6) rgba(255,255,255,0.1);
            }
            
            /* Dropdown z-index fix */
            .Select {
                z-index: 1000 !important;
                position: relative;
            }
            .Select-control {
                background-color: rgba(20, 25, 35, 0.95) !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
                border-radius: 8px !important;
            }
            .Select-value-label,
            .Select-placeholder,
            .Select-input > input {
                color: #e2e8f0 !important;
                font-weight: 500;
            }
            .Select-menu-outer {
                background-color: rgba(20, 25, 35, 0.98) !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
                border-radius: 8px !important;
                z-index: 1001 !important;
                position: absolute !important;
            }
            .Select-option {
                background-color: transparent !important;
                color: #e2e8f0 !important;
                font-weight: 500;
            }
            .Select-option:hover {
                background-color: rgba(66, 153, 225, 0.3) !important;
            }
            .Select-option.is-focused {
                background-color: rgba(66, 153, 225, 0.2) !important;
            }
            
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .dashboard-container {
                height: 100vh;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H3("🌤️ Weather Dashboard", 
                   style={'color': 'white', 'marginBottom': '5px', 'fontWeight': '600', 
                          'textShadow': '0 2px 4px rgba(0,0,0,0.3)'}),
            html.P("Real-time weather visualization for major Indian cities", 
                  style={'fontSize': '14px', 'opacity': '0.9', 'margin': '0', 
                         'textShadow': '0 1px 2px rgba(0,0,0,0.3)'})
        ], width=8),
        dbc.Col([
            dcc.Dropdown(
                id='city-select',
                options=[{'label': k, 'value': k} for k in INDIAN_CITIES.keys()],
                value='Mumbai',
                clearable=False,
                style={
                    'backgroundColor': 'rgba(20, 25, 35, 0.95)', 
                    'border': '1px solid rgba(255,255,255,0.3)',
                    'color': COLORS['text'],
                    'borderRadius': '8px',
                    'zIndex': '1000'
                }
            )
        ], width=4, style={'position': 'relative', 'zIndex': '1000'})
    ], style={'padding': '15px 0 25px 0', 'marginBottom': '10px', 'position': 'relative', 'zIndex': '1000'}),
    
    # Main Content Row
    dbc.Row([
        # Left Column - Current Weather
        dbc.Col([
            # City Name and Time Card
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='city-name', style={'fontSize': '24px', 'fontWeight': '600', 
                                                   'marginBottom': '8px', 'color': 'white'}),
                    html.Div(id='current-time', style={'fontSize': '14px', 'opacity': '0.9'})
                ], style={'padding': '20px', 'textAlign': 'center'})
            ], style={'backgroundColor': COLORS['card'], 'border': '1px solid rgba(255,255,255,0.15)', 
                     'borderRadius': '12px', 'marginBottom': '20px', 'minHeight': '100px'}),
            
            # Main Temperature Card
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='main-temp', style={'fontSize': '72px', 'fontWeight': '300', 'margin': '0', 
                                                   'lineHeight': '1', 'color': 'white'}),
                    html.Div(id='weather-desc', style={'fontSize': '18px', 'opacity': '0.9', 
                                                      'marginTop': '12px', 'marginBottom': '8px'}),
                    html.Div(id='feels-like', style={'fontSize': '14px', 'opacity': '0.8'})
                ], style={'padding': '30px', 'textAlign': 'center'})
            ], style={'backgroundColor': COLORS['card'], 'border': '1px solid rgba(255,255,255,0.15)', 
                     'borderRadius': '12px', 'marginBottom': '20px', 'minHeight': '200px'}),
            
            # Weather Metrics Grid
            dbc.Row([
                dbc.Col(html.Div(id='humidity-card'), width=6, style={'marginBottom': '15px', 'padding': '0 8px'}),
                dbc.Col(html.Div(id='wind-card'), width=6, style={'marginBottom': '15px', 'padding': '0 8px'}),
                dbc.Col(html.Div(id='pressure-card'), width=6, style={'marginBottom': '15px', 'padding': '0 8px'}),
                dbc.Col(html.Div(id='visibility-card'), width=6, style={'marginBottom': '15px', 'padding': '0 8px'})
            ], style={'marginTop': '5px'})
        ], width=4, style={'display': 'flex', 'flexDirection': 'column', 'height': 'calc(100vh - 180px)'}),
        
        # Right Column - Forecasts and Charts
        dbc.Col([
            # Weekly Overview - Fixed frame with increased height
            dbc.Card([
                dbc.CardBody([
                    html.H6("7-Day Forecast", style={'marginBottom': '20px', 'fontWeight': '600', 
                                                   'fontSize': '18px', 'color': 'white'}),
                    html.Div(id='weekly-forecast', style={'width': '100%', 'overflow': 'hidden'})
                ], style={'padding': '25px', 'height': '100%'})
            ], style={'backgroundColor': COLORS['card'], 'border': '1px solid rgba(255,255,255,0.15)', 
                     'borderRadius': '12px', 'marginBottom': '20px', 'height': '180px'}),
            
            # Temperature Chart with adjusted height
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='temp-chart', config={'displayModeBar': False})
                ], style={'padding': '15px'})
            ], style={'backgroundColor': COLORS['card'], 'border': '1px solid rgba(255,255,255,0.15)', 
                     'borderRadius': '12px', 'height': '340px'})
        ], width=8, style={'display': 'flex', 'flexDirection': 'column', 'height': 'calc(100vh - 180px)', 'gap': '20px'})
    ], style={'height': 'calc(100vh - 180px)'}),
    
    # Auto-refresh every 5 minutes
    dcc.Interval(id='refresh', interval=5*60*1000, n_intervals=0)
    
], fluid=True, id='main-container', className='dashboard-container', style={'position': 'relative'})

# Callback to update all dashboard components
@app.callback(
    [Output('city-name', 'children'),
     Output('current-time', 'children'),
     Output('main-temp', 'children'),
     Output('weather-desc', 'children'),
     Output('feels-like', 'children'),
     Output('humidity-card', 'children'),
     Output('wind-card', 'children'),
     Output('pressure-card', 'children'),
     Output('visibility-card', 'children'),
     Output('weekly-forecast', 'children'),
     Output('temp-chart', 'figure'),
     Output('main-container', 'style')],
    [Input('city-select', 'value'),
     Input('refresh', 'n_intervals')]
)
def update_dashboard(city, n):
    """Update all dashboard components with current weather data"""
    try:
        city_info = INDIAN_CITIES[city]
        
        # Get current time for the city
        tz = pytz.timezone(city_info['tz'])
        current_time = datetime.now(tz)
        current_hour = current_time.hour
        time_str = current_time.strftime('%I:%M %p, %B %d, %Y')
        
        # Fetch weather data
        weather = get_weather(city_info['lat'], city_info['lon'])
        forecasts = get_forecast(city_info['lat'], city_info['lon'])
        
        if not weather:
            # Return default background when no data
            bg_style = get_background_style('clear', current_hour)
            return [city, time_str, "--°C"] + ["No Data"] * 8 + [bg_style]
        
        # Get dynamic background style
        bg_style = get_background_style(weather['description'], current_hour)
        
        return [
            city,
            time_str,
            f"{weather['temp']}°C",
            weather['description'],
            f"Feels like {weather['feels_like']}°C",
            create_metric_card('💧', 'Humidity', weather['humidity'], '%'),
            create_metric_card('💨', 'Wind Speed', weather['wind_speed'], 'km/h'),
            create_metric_card('🌡️', 'Pressure', weather['pressure'], 'hPa'),
            create_metric_card('👁️', 'Visibility', weather['visibility'], 'km'),
            create_weekly_overview(forecasts),
            create_temp_chart(forecasts),
            bg_style
        ]
    except Exception as e:
        print(f"Dashboard Update Error: {e}")
        # Return default background on error
        bg_style = get_background_style('clear', 12)
        return [city, "Error loading time", "--°C"] + ["Error"] * 8 + [bg_style]

# Run the application
if __name__ == '__main__':
    print("=" * 70)
    print("🌤️  INDIA WEATHER DASHBOARD STARTING...")
    print("=" * 70)
    print("✨ Dashboard available at: http://127.0.0.1:8050/")
    print("💡 Press CTRL+C to stop the server")
    print("=" * 70)
    app.run(debug=True, port=8050)