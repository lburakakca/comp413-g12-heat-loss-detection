import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import threading
import time
import requests
import pandas as pd
import dash_bootstrap_components as dbc

# ESP32 IP
ESP32_IP = "192.168.4.1"
SENSOR_ENDPOINT = f"http://{ESP32_IP}/sensorData"

sensor_data = {
    "time": [],
    "sensor1": {"temp": [], "humidity": []},
    "sensor2": {"temp": [], "humidity": []},
    "sensor3": {"temp": [], "humidity": []},
}

def fetch_sensor_data():
    global sensor_data
    while True:
        try:
            response = requests.get(SENSOR_ENDPOINT)
            if response.status_code == 200:
                data = response.json()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                sensor_data["time"].append(timestamp)
                for sensor in ["sensor1", "sensor2", "sensor3"]:
                    sensor_data[sensor]["temp"].append(data[sensor]["temp"])
                    sensor_data[sensor]["humidity"].append(data[sensor]["humidity"])
        except Exception as e:
            print(f"Error fetching data: {e}")
        time.sleep(5)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Heat Loss Detection",
        color="primary",
        dark=True,
        fluid=True
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    html.H4("Sensor 1", className="card-title"),
                    html.P(id="sensor1-temp", className="card-text"),
                    html.P(id="sensor1-humidity", className="card-text"),
                ],
                id="sensor1-card",
                color="light",
                inverse=False,
                className="mb-3"
            )
        ]),
        dbc.Col([
            dbc.Card(
                [
                    html.H4("Sensor 2", className="card-title"),
                    html.P(id="sensor2-temp", className="card-text"),
                    html.P(id="sensor2-humidity", className="card-text"),
                ],
                id="sensor2-card",
                color="light",
                inverse=False,
                className="mb-3"
            )
        ]),
        dbc.Col([
            dbc.Card(
                [
                    html.H4("Sensor 3", className="card-title"),
                    html.P(id="sensor3-temp", className="card-text"),
                    html.P(id="sensor3-humidity", className="card-text"),
                ],
                id="sensor3-card",
                
                color="light",
                inverse=False,
                className="mb-3"
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Set Temperature Threshold (°C):"),
            dcc.Input(id="temp-threshold", type="number", value=45, style={"margin-bottom": "10px"}),
            html.Button("Download Data", id="download-button", className="btn btn-secondary"),
            dcc.Download(id="download-data")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="temp-chart"), width=12)
    ]),
    dcc.Interval(
        id="interval-component",
        interval=2000,  
        n_intervals=0
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Heat Loss Alert"),
            dbc.ModalBody(id="modal-body"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="btn btn-primary", n_clicks=0)
            ),
        ],
        id="heat-loss-modal",
        is_open=False,
    )
], fluid=True)

# Callbacks
@app.callback(
    [
        Output("sensor1-temp", "children"),
        Output("sensor1-humidity", "children"),
        Output("sensor2-temp", "children"),
        Output("sensor2-humidity", "children"),
        Output("sensor3-temp", "children"),
        Output("sensor3-humidity", "children"),
        Output("temp-chart", "figure"),
        Output("heat-loss-modal", "is_open"),
        Output("modal-body", "children"),
    ],
    [Input("interval-component", "n_intervals"),
     Input("temp-threshold", "value"),
     Input("close-modal", "n_clicks")],
    [State("heat-loss-modal", "is_open")]
)
def update_dashboard(n, temp_threshold, close_clicks, is_open):
    alert_message = ""
    show_modal = False

    for sensor in ["sensor1", "sensor2", "sensor3"]:
        if sensor_data[sensor]["temp"] and sensor_data[sensor]["temp"][-1] > temp_threshold:
            alert_message = f"Heat loss detected! {sensor} exceeded {temp_threshold} °C."
            show_modal = True

    if close_clicks > 0:
        show_modal = False

    figure = {
        "data": [
            {"x": sensor_data["time"], "y": sensor_data["sensor1"]["temp"], "type": "line", "name": "Sensor 1", "line": {"color": "blue", "dash": "solid"}},
            {"x": sensor_data["time"], "y": sensor_data["sensor2"]["temp"], "type": "line", "name": "Sensor 2", "line": {"color": "green", "dash": "dash"}},
            {"x": sensor_data["time"], "y": sensor_data["sensor3"]["temp"], "type": "line", "name": "Sensor 3", "line": {"color": "red", "dash": "dot"}}
        ],
        "layout": {
            "title": "Temperature Over Time",
            "yaxis": {"title": "Temperature (°C)"},
            "xaxis": {"title": "Time"}
        }
    }
    return (
        f"Temperature: {sensor_data['sensor1']['temp'][-1]} °C" if sensor_data["sensor1"]["temp"] else "No Data",
        f"Humidity: {sensor_data['sensor1']['humidity'][-1]} %" if sensor_data["sensor1"]["humidity"] else "No Data",
        f"Temperature: {sensor_data['sensor2']['temp'][-1]} °C" if sensor_data["sensor2"]["temp"] else "No Data",
        f"Humidity: {sensor_data['sensor2']['humidity'][-1]} %" if sensor_data["sensor2"]["humidity"] else "No Data",
        f"Temperature: {sensor_data['sensor3']['temp'][-1]} °C" if sensor_data["sensor3"]["temp"] else "No Data",
        f"Humidity: {sensor_data['sensor3']['humidity'][-1]} %" if sensor_data["sensor3"]["humidity"] else "No Data",
        figure,
        show_modal,
        alert_message
    )

@app.callback(
    Output("download-data", "data"),
    [Input("download-button", "n_clicks")]
)
def download_data(n_clicks):
    if n_clicks:
        df = pd.DataFrame({
            "Time": sensor_data["time"],
            "Sensor 1 Temp (°C)": sensor_data["sensor1"]["temp"],
            "Sensor 2 Temp (°C)": sensor_data["sensor2"]["temp"],
            "Sensor 3 Temp (°C)": sensor_data["sensor3"]["temp"],
        })
        return dcc.send_data_frame(df.to_csv, "heat_loss_data.csv")

sensor_thread = threading.Thread(target=fetch_sensor_data, daemon=True)
sensor_thread.start()

if __name__ == "__main__":
    app.run_server(debug=True)
