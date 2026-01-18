-- Final production ingestion using ClickHouse Kafka Engine + Materialized View

CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.api_events (
    event_time DateTime,
    user_id String,
    endpoint String,
    status_code UInt16,
    latency_ms UInt32
)
ENGINE = MergeTree()
PARTITION BY toDate(event_time)
ORDER BY (endpoint, event_time);

DROP VIEW IF EXISTS analytics.api_events_mv;
DROP TABLE IF EXISTS analytics.api_events_kafka;

CREATE TABLE analytics.api_events_kafka (
    event_time DateTime,
    user_id String,
    endpoint String,
    status_code UInt16,
    latency_ms UInt32
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'api-events',
    kafka_group_name = 'clickhouse-api-events',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1;

CREATE MATERIALIZED VIEW analytics.api_events_mv
TO analytics.api_events
AS
SELECT
    event_time,
    user_id,
    endpoint,
    status_code,
    latency_ms
FROM analytics.api_events_kafka;
