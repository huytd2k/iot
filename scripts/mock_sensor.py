import random
import time

from paho.mqtt import client as mqtt_client

broker = "broker.hivemq.com"
port = 1883
topic = "/clientPub"
# generate client ID with pub prefix randomly
client_id = f"{random.randint(0, 100)}"
username = "quyhot"
password = ""


def publish(client):
    while True:
        time.sleep(1)
        msg = f"mock-device/{80-random.randint(0,10)}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print("success")
        else:
            print("false")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()
