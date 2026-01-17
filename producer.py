import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

endpoints = ["/api/login", "/api/payments", "/api/refunds"]

while True:
    event = {
        "event_time": datetime.utcnow().isoformat(),
        "user_id": f"user_{random.randint(1, 100)}",
        "endpoint": random.choice(endpoints),
        "status_code": random.choice([200, 200, 200, 500]),
        "latency_ms": random.randint(20, 800)
    }

    producer.send("api-events", event)
    print(event)
    time.sleep(0.3)

