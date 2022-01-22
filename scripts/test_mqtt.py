import random

from paho.mqtt import client as mqtt_client


broker = "broker.hivemq.com"
port = 1883
topic = "/clientPub"
# generate client ID with pub prefix randomly
client_id = f"{random.randint(0, 100)}"
username = "quyhot"
password = ""


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"topic {msg.topic} : {msg.payload.decode()}")

    client.subscribe(topic)
    client.on_message = on_message


def connect_mqtt() -> mqtt_client:
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
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
