import paho.mqtt.client as mqtt

# Define the MQTT server details
MQTT_BROKER = "192.168.0.32"  # Replace with the host address of your MQTT server
MQTT_PORT = 1883  # Default port for MQTT is 1883
MQTT_TOPICS = [("/temperature",0),("/moisture",0),("/humidity",0)]  # Topic to subscribe to

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the desired topic upon successful connection
        client.subscribe(MQTT_TOPICS)
        print(f"Subscribed to topic '{MQTT_TOPICS}'")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    # This callback will be called for every message received on subscribed topics
    print(f"Received message from topic '{msg.topic}': {msg.payload.decode()}")

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