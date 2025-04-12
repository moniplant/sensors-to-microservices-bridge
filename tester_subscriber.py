import paho.mqtt.client as mqtt
import yaml
import requests
import time
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:3000")

# Define the MQTT server details
MQTT_BROKER = os.getenv("MQTT_BROKER", "192.168.0.32")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

with open('config.yml', 'r') as yaml_file:
    content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    topic_names = [
        f'/{content["PLANT_TOKEN"]}/{content["SENSORS_TOKENS"]["MOISTURE_TOKEN"]}', 
        f'/{content["PLANT_TOKEN"]}/{content["SENSORS_TOKENS"]["HUMIDITY_TOKEN"]}', 
        f'/{content["PLANT_TOKEN"]}/{content["SENSORS_TOKENS"]["TEMPERATURE_TOKEN"]}'
    ]
    MQTT_TOPICS = list(map(lambda x: (x, 0), topic_names))

def send_data_to_api(plant_id, sensor_id, value):
    """
    Sends a POST request to /plant endpoint with given plant JSON data.

    Parameters:
        json_string (str): JSON-formatted string containing plant data.
        base_url (str): Base URL of the API (default is placeholder).

    Returns:
        Response object
    """
    url = f"{API_URL}/sensor/sensorData"

    try:
        # Create the payload
        payload = {
            "plant_id": plant_id,
            "sensor_id": sensor_id,
            "timestamp": time.time(),  # Current time in seconds since epoch
            "value": value
        }

        # Send the POST request
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 201 or response.status_code == 200:
            print("✅ Data sent successfully")
        else:
            print(f"⚠️ Failed to send data: {response.status_code}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the desired topic upon successful connection
        client.subscribe(MQTT_TOPICS)
        print(f"Subscribed to topic '{MQTT_TOPICS}'")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):

    # Extract the plant ID and sensor ID from the topic
    topic_parts = msg.topic.split('/')
    plant_id = topic_parts[1]  # Assuming the second part is the plant ID
    sensor_id = topic_parts[2]  # Assuming the third part is the sensor ID
    # Decode the message payload
    value = msg.payload.decode()
    # This callback will be called for every message received on subscribed topics
    print(f"Received message from plant '{plant_id}' and sensor '{sensor_id}': {value}")
    send_data_to_api(plant_id, sensor_id, value)

def main():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Attach the on_connect and on_message callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    try:
        print("Connecting to MQTT broker...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        # Start the network loop
        client.loop_forever()  # This will keep the script running to listen for messages
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()