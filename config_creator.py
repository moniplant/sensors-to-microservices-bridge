import json
import yaml
import requests

API_URL="http://localhost:3000"

with open("config.yml", "r") as yaml_file:
    content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    plant_token = content["PLANT_TOKEN"]
    humidty_sensor_token = content["SENSORS_TOKENS"]["HUMIDITY_TOKEN"]
    temperature_sensor_token = content["SENSORS_TOKENS"]["TEMPERATURE_TOKEN"]
    moisture_sensor_token = content["SENSORS_TOKENS"]["MOISTURE_TOKEN"]


def create_plant_payload(
    plant_id, plant_name, plant_description, location, plant_type, adoption_date
):
    return json.dumps(
        {
            "plant_id": plant_id,
            "plant_name": plant_name,
            "plant_description": plant_description,
            "plant_location": location,
            "plant_type": plant_type,
            "adoption_date": adoption_date,
        }
    )

def create_sensor_payload(
    sensor_id, label, plant_id, quantity, unit
):
    return json.dumps(
        {
            "sensor_id": sensor_id,
            "label": label,
            "plant_id": plant_id,
            "quantity": quantity,
            "unit": unit,
        }
    )

def create_plant(json_string):
    """
    Sends a POST request to /plant endpoint with given plant JSON data.

    Parameters:
        json_string (str): JSON-formatted string containing plant data.
        base_url (str): Base URL of the API (default is placeholder).

    Returns:
        Response object
    """
    url = f"{API_URL}/plant"

    try:
        # Convert the string to a Python dict
        plant_data = json.loads(json_string)

        # Send the POST request
        response = requests.post(url, json=plant_data)

        # Check response
        if response.status_code == 201 or response.status_code == 200:
            print("✅ Plant created successfully!")
        else:
            print(f"⚠️ Failed to create plant. Status code: {response.status_code}")
            print("Response:", response.text)

        return response

    except json.JSONDecodeError as e:
        print("❌ Invalid JSON string:", e)
    except requests.RequestException as e:
        print("❌ Request failed:", e)

def create_sensor(json_string):
    """
    Sends a POST request to /sensor endpoint with given sensor JSON data.

    Parameters:
        json_string (str): JSON-formatted string containing sensor data.
        base_url (str): Base URL of the API (default is placeholder).

    Returns:
        Response object
    """
    url = f"{API_URL}/sensor"

    try:
        # Convert the string to a Python dict
        sensor_data = json.loads(json_string)

        # Send the POST request
        response = requests.post(url, json=sensor_data)

        # Check response
        if response.status_code == 201 or response.status_code == 200:
            print("✅ Sensor created successfully!")
        else:
            print(f"⚠️ Failed to create sensor. Status code: {response.status_code}")
            print("Response:", response.text)

        return response

    except json.JSONDecodeError as e:
        print("❌ Invalid JSON string:", e)
    except requests.RequestException as e:
        print("❌ Request failed:", e)


if __name__ == "__main__":

    create_plant(
        create_plant_payload(
            plant_id=plant_token,
            plant_name="My Avocado Tree",
            plant_description="This specific tree needs more attenstion, since it needs a lot of water",
            location="Living Room",
            plant_type="Persea",
            adoption_date="2024-06-15",
        )
    )

    create_sensor(
        create_sensor_payload(
            sensor_id=humidty_sensor_token,
            label="Humidity Sensor",
            plant_id=plant_token,
            quantity="Ratio",
            unit="%",
        )
    )

    create_sensor(
        create_sensor_payload(
            sensor_id=temperature_sensor_token,
            label="Temperature Sensor",
            plant_id=plant_token,
            quantity="Temperature",
            unit="°C",
        )
    )

    create_sensor(
        create_sensor_payload(
            sensor_id=moisture_sensor_token,
            label="Moisture Sensor",
            plant_id=plant_token,
            quantity="Ratio",
            unit="%",
        )
    )
