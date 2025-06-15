import paho.mqtt.client as mqtt
import numpy as np
import json
import time
from datetime import datetime

broker = "localhost"
topic = "sensor/data"

client = mqtt.Client()
client.connect(broker)

print("Publisher started...")

for i in range(60):  # 1 minute of data
    temperature = round(np.random.uniform(24, 36), 2)
    humidity = round(np.random.uniform(38, 87), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp
    }

    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"Published: {payload}")
    time.sleep(1)

client.disconnect()
