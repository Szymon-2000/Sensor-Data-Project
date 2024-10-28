# Sensor-Data-Project
## Project Description
This project generates and processes data related to temperature and humidity. It uses Apache Kafka as a tool for real-time data streaming. Data is generated using `sensor_data_generator.py` and then processed and displayed in a chart by `sensor_data_processor.py`.

## Requirements
- Python 3.x
- Apache Kafka
- Zookeeper

## How to Run the Project

1. **Start Zookeeper and Kafka**:
   - In a terminal, start Zookeeper:
     ```bash
     zookeeper-server-start.sh config/zookeeper.properties
     ```
   - Then, start the Kafka Server:
     ```bash
     kafka-server-start.sh config/server.properties
     ```

2. **Create a topic in Kafka**:
   ```bash
   kafka-topics.sh --create --topic sensor-data --bootstrap-server localhost:9092
