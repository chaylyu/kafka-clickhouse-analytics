import json
from kafka import KafkaConsumer
from datetime import datetime
import clickhouse_connect
import time
import signal
import sys

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    database="analytics"
)

consumer = KafkaConsumer(
    "api-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

batch = []
BATCH_SIZE = 100
FLUSH_INTERVAL = 5  # seconds
last_flush = time.time()

for msg in consumer:
    e = msg.value
    batch.append((
        datetime.fromisoformat(e["event_time"]),
        e["user_id"],
        e["endpoint"],
        e["status_code"],
        e["latency_ms"]
    ))

    now = time.time()

    if len(batch) >= BATCH_SIZE or (now - last_flush) >= FLUSH_INTERVAL:
        client.insert(
            "api_events",
            batch,
            column_names=[
                "event_time",
                "user_id",
                "endpoint",
                "status_code",
                "latency_ms"
            ]
        )
        print(f"Inserted {len(batch)} rows")
        batch.clear()
        last_flush = now
    
def shutdown(sig, frame):
    if batch:
        client.insert(
            "api_events",
            batch,
            column_names=[
                "event_time",
                "user_id",
                "endpoint",
                "status_code",
                "latency_ms"
            ]
        )
        print(f"Flushed {len(batch)} rows on shutdown")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)
