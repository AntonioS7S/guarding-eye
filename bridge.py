import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

MQTT_BROKER = "localhost"
MQTT_TOPIC  = "guarding-eye/sensor"
INFLUX_DB   = "guardingeyedb"

influx = InfluxDBClient(host="localhost", port=8086, database=INFLUX_DB)

def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    print(f"Received: {value}%")
    influx.write_points([{
        "measurement": "sensor",
        "fields": {"value": value}
    }])

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)
client.loop_forever()

