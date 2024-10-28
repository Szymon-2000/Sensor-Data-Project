from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_data():
    while True:
        sensor_data = {
            'sensor_id': random.randint(1, 5),
            'temperature': round(random.uniform(20.0, 25.0), 2),
            'humidity': round(random.uniform(40.0, 50.0), 2),
            'timestamp': datetime.now().isoformat()
        }
        producer.send('sensor-data', sensor_data)
        print(f"Sent data: {sensor_data}")
        time.sleep(2)

if __name__ == "__main__":
    generate_data()
