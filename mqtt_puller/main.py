from datetime import datetime
import random

from influxdb_client import InfluxDBClient, Point, WritePrecision
from paho.mqtt import client as mqtt_client
import requests
import smtplib, ssl


def send_email(msg):
    port = 465  # For SSL
    password = ""

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("huytran2khust@gmail.com", password)
        server.sendmail("huytran2khust@gmail.com", "huytd2k@gmail.com", msg)
        print("SENT")


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

    def on_message(client, userdata, msg: mqtt_client.MQTTMessage):
        msg = msg.payload.decode("utf-8")
        device_id = msg.split("/")[0]
        heartbeat = int(msg.split("/")[1])
        patient = requests.get(f"http://localhost:8000/api/patient/{device_id}").json()

        if patient:
            if heartbeat < patient['heartrate_threshhold']:
                send_email(f"Patient with device {device_id} is with heartrate {heartbeat} below threshhold {patient['heartrate_threshhold']}")

        point = (
            Point("heartbeat")
            .tag("device", device_id)
            .field("heartbeat", heartbeat)
            .time(datetime.utcnow(), WritePrecision.NS)
        )
        write_api.write("iot", "iot", point)
        print(f"Write {msg} to influxDB")

    client.subscribe(topic)
    client.on_message = on_message


if __name__ == "__main__":
    dbclient = InfluxDBClient(
        "http://localhost:8086",
        token="BCzq6pkHR96UjaMbqys78hsHG8IaaJ6Ij9TjiJd_u-I7Bt3-tTPx68tvpbyve-unCEEGrjqDtGLi_SxaFAlRTw==",
    )
    client = connect_mqtt()
    subscribe(client, dbclient)
    client.loop_forever()
