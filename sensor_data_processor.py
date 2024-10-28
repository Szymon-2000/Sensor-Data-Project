from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import deque

consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sensor-group'
)

# Tutaj przechowujemy tylko ostatnie 30 punktów danych
max_points = 30
timestamps = deque(maxlen=max_points)
temperatures = deque(maxlen=max_points)
humidities = deque(maxlen=max_points)
alert_timestamps_temp = deque(maxlen=max_points)
alert_temperatures = deque(maxlen=max_points)
alert_timestamps_hum = deque(maxlen=max_points)
alert_humidities = deque(maxlen=max_points)

# Alerty
temperature_alert_threshold = 24.5
humidity_alert_threshold = 48.0  

# Wykres
plt.ion()
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

def process_data(data):
    print(f"Raw data: {data}")
    
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    
    timestamp = datetime.fromisoformat(data['timestamp'])
    temperature = data['temperature']
    humidity = data['humidity']
    
    timestamps.append(timestamp)
    temperatures.append(temperature)
    humidities.append(humidity)
    
    if temperature > temperature_alert_threshold:
        print(f"ALERT! High temperature detected: {temperature} at {data['timestamp']}")
        alert_timestamps_temp.append(timestamp)
        alert_temperatures.append(temperature)
    
    if humidity > humidity_alert_threshold:
        print(f"ALERT! High humidity detected: {humidity} at {data['timestamp']}")
        alert_timestamps_hum.append(timestamp)
        alert_humidities.append(humidity)

def update_plot():
    ax1.clear()
    ax2.clear()
    
    ax1.plot(timestamps, temperatures, label="Temperature", color='tab:blue')
    ax1.scatter(alert_timestamps_temp, alert_temperatures, color='red', label="Temperature Alerts", s=50, marker='o')
    ax1.axhline(y=temperature_alert_threshold, color='gray', linestyle='--', linewidth=0.5)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    
    ax2.plot(timestamps, humidities, label="Humidity", color='tab:green')
    ax2.scatter(alert_timestamps_hum, alert_humidities, color='orange', label="Humidity Alerts", s=50, marker='x')
    ax2.axhline(y=humidity_alert_threshold, color='gray', linestyle='--', linewidth=0.5)
    ax2.set_ylabel('Humidity (%)', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    
    if len(timestamps) > 0:
        ax1.set_xlim([min(timestamps), max(timestamps)])
    
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.draw()
    plt.pause(0.5)  

if __name__ == "__main__":
    print("Starting data processing loop...")
    try:
        while True:
            message = next(consumer)
            data = message.value.decode('utf-8')
            process_data(data)
            update_plot()
    except KeyboardInterrupt:
        pass  
    
    print("Data processing loop ended.")
    plt.show(block=True)  # Blokowanie, aby okno pozostało otwarte
