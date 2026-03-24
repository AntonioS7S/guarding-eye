# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack & Services

All infrastructure runs via Docker Compose:

```bash
docker compose up -d       # Start all services
docker compose down        # Stop all services
docker compose logs -f     # Follow logs
```

| Service    | Port | Purpose                        |
|------------|------|--------------------------------|
| Mosquitto  | 1883 | MQTT broker (sensor ingestion) |
| InfluxDB   | 8086 | Time-series storage            |
| Grafana    | 3000 | Visualization dashboards       |
| Node-RED   | 1880 | Flow-based automation          |
| Portainer  | 9000 | Docker management UI           |

## Running the Bridge

`bridge.py` requires `paho-mqtt` and `influxdb` Python packages. Run it **outside** Docker (on the host or Pi):

```bash
pip install paho-mqtt influxdb
python bridge.py
```

The bridge connects to Mosquitto on `localhost:1883` and InfluxDB on `localhost:8086`. If running inside Docker, update `MQTT_BROKER` and the InfluxDB host to use Docker service names (`mosquitto`, `influxdb`).

## Architecture

**Data flow:**

```
Pi Pico W (sensor) → MQTT topic guarding-eye/sensor → Mosquitto → bridge.py → InfluxDB → Grafana
```

- The Pi Pico W publishes a single float value (percentage) to `guarding-eye/sensor`.
- `bridge.py` subscribes to that topic and writes each reading as a `sensor` measurement with a `value` field to the `guardingeyedb` InfluxDB database.
- Grafana queries InfluxDB to display readings. Node-RED can add alerting/automation logic.

## Key Configuration

- **MQTT topic:** `guarding-eye/sensor`
- **InfluxDB database:** `guardingeyedb`
- **Mosquitto:** anonymous access enabled, persistence at `/mosquitto/data/`
- Mosquitto config: `mosquitto/config/mosquitto.conf`
