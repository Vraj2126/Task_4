import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import json
import csv

#  Use a clean built-in style
plt.style.use('ggplot')

# Data storage
timestamps = []
temperatures = []
humidities = []

# MQTT setup
broker_address = "localhost"
topic = "sensor/data"

# Callback when connected to broker
def on_connect(client, userdata, flags, rc):
    print(f" Subscriber connected with result code {rc}")
    client.subscribe(topic)

# Callback when message received
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f" Received: {data}")

        # Parse and append data
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        temp = data["temperature"]
        hum = data["humidity"]

        timestamps.append(timestamp)
        temperatures.append(temp)
        humidities.append(hum)

        # Log to CSV
        with open("sensor_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, temp, hum])

    except Exception as e:
        print(f" Error processing message: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, 1883, 60)
client.loop_start()

# Plot setup
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("Real-Time IoT Sensor Data (Temperature & Humidity)", fontsize=14)

def animate(i):
    ax1.clear()
    ax2.clear()

    ax1.plot(timestamps, temperatures, color='red', marker='o', label="Temperature (°C)")
    ax2.plot(timestamps, humidities, color='blue', marker='o', label="Humidity (%)")

    ax1.set_ylabel("Temperature (°C)")
    ax2.set_ylabel("Humidity (%)")
    ax2.set_xlabel("Time")

    ax1.set_ylim(20, 40)   # Adjusted for realistic temperature range
    ax2.set_ylim(30, 90)   # Adjusted for realistic humidity range

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper left")

    for label in ax1.get_xticklabels():
        label.set_rotation(30)
    for label in ax2.get_xticklabels():
        label.set_rotation(30)

    plt.tight_layout()

# FIXED: limit frame cache to avoid warning
ani = FuncAnimation(fig, animate, interval=1000, save_count=60)

# Start plotting
plt.show()
