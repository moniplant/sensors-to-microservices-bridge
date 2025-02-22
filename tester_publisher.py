import paho.mqtt.client as mqtt

# Define the MQTT server details
MQTT_BROKER = "192.168.0.32"  # Replace with the host address of your MQTT server
MQTT_PORT = 1883  # Default port for MQTT is 1883
MQTT_TOPIC = "/topic/qos0"  # Topic to publish to

# Define the message to publish
MESSAGE = "Hello World"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Publish the message upon successful connection
        client.publish(MQTT_TOPIC, MESSAGE)
        print(f"Message '{MESSAGE}' published to topic '{MQTT_TOPIC}'")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Attach the on_connect callback
    client.on_connect = on_connect

    # Connect to the MQTT broker
    try:
        print("Connecting to MQTT broker...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Start the network loop
        client.loop_start()
        
        # Allow time for the message to be sent
        import time
        time.sleep(2)

        # Stop the network loop and disconnect
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
