import paho.mqtt.client as mqtt

# MQTT Broker Settings
broker_address = "your_mqtt_broker_address"
broker_port = "port"
username = "your_mqtt_username"
password = "your_mqtt_password"

# Topic to Subscribe
tupper_measurement_topic = "tupperiot/device/+/measurement"

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create MQTT Client
client = mqtt.Client("TupperIoT_Subscriber")

client.username_pw_set(username, password)

client.on_message = on_message
client.connect(broker_address, broker_port)

# Subscribe to the Tupper IoT measurement topic
client.subscribe(tupper_measurement_topic)

# Loop to continuously listen for messages
client.loop_forever()
