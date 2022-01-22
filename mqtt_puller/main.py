from datetime import datetime
import random

from influxdb_client import InfluxDBClient, Point, WritePrecision
from paho.mqtt import client as mqtt_client


broker = "broker.hivemq.com"
port = 1883
topic = "/clientPub"
# generate client ID with pub prefix randomly
client_id = f"{random.randint(0, 100)}"
username = "quyhot"
password = ""


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


def subscribe(client: mqtt_client, influx_client: InfluxDBClient):
    write_api = influx_client.write_api()

    def on_message(client, userdata, msg):
        point = (
            Point("heartbeat")
            .tag("host", "host1")
            .field("heartbeat", int(msg.payload.decode()))
            .time(datetime.utcnow(), WritePrecision.NS)
        )
        write_api.write("iot", "iot", point)
        print(f"write {msg.payload.decode()}")

    client.subscribe(topic)
    client.on_message = on_message


if __name__ == "__main__":
    dbclient = InfluxDBClient(
        "http://localhost:8086",
        token="ba2ZkeaUNZnL8WjKlFXOadNHMQzrubbYvxhUjH1ioz1Tjw2tvymkJLxHqxecuvqqJyEIfoXMg0chYSbK-JfDNg==",
    )
    client = connect_mqtt()
    subscribe(client, dbclient)
    client.loop_forever()
