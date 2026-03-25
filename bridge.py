import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

MQTT_BROKER = "localhost"
MQTT_TOPIC  = "guarding-eye/sensor"
INFLUX_DB   = "guardingeyedb"

influx = InfluxDBClient(host="localhost", port=8086, database=INFLUX_DB)

def on_message(client, userdata, msg):
    try:
        parts = msg.payload.decode().split(",")
        temp  = float(parts[0])
        humid = float(parts[1])
        volt  = float(parts[2])
        print(f"Received: T={temp}% H={humid}% V={volt}%")
        influx.write_points([{
            "measurement": "sensor",
            "fields": {
                "temperature": temp,
                "humidity":    humid,
                "voltage":     volt
            }
        }])
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883)
client.subscribe(MQTT_TOPIC)
client.loop_forever()
