import paho.mqtt.client as mqtt
import time
import random
from credentials import mqtt_username, mqtt_password, host, port

# MQTT broker configuration
broker = host

# List of device UIDs
device_uids = ["123456", "234567", "345678"]

# Function to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Successfully connected to broker (RC: {rc})")
    else:
        print(f"Failed to connect (RC: {rc})")

# Function for disconnection
def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

# Create MQTT clients for each device
clients = [mqtt.Client(f"trims_{uid}") for uid in device_uids]

# Configuration for each client
for client, uid in zip(clients, device_uids):
    client.username_pw_set(mqtt_username, mqtt_password)  # Set username and password
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # Set the Last Will and Testament (LWT)
    client.will_set(f"tupperiot/device/{uid}/status", "OFF", qos=1, retain=True)

    client.connect(broker, port, 60)
    client.loop_start()

    # Publish "ON" message at start
    client.publish(f"tupperiot/device/{uid}/status", "ON", qos=1, retain=True)

# Function to simulate data sending
def simulate_data():
    try:
        while True:
            for client, uid in zip(clients, device_uids):
                # Simulate measurement of product percentage
                percentage = random.randint(0, 100)
                client.publish(f"tupperiot/device/{uid}/measurement", percentage, retain=True)

            # Wait a minute before sending the next set of messages
            time.sleep(60)
    except KeyboardInterrupt:
        print("Simulation interrupted")
    finally:
        # Disconnect the clients
        for client in clients:
            client.loop_stop()
            client.disconnect()

# Start the simulation
simulate_data()
