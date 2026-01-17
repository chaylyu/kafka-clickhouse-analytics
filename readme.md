# Kafka → ClickHouse Real-Time Analytics Pipeline

## Overview
This project implements a real-time streaming analytics pipeline using **Kafka** and **ClickHouse**.
It simulates API usage events, ingests them via Kafka, processes them with a Python consumer, and stores them in ClickHouse for 
low-latency analytical queries.

The goal of the project is to demonstrate production-minded data engineering concepts such as streaming ingestion, batching strategies, 
and analytical data modeling.

---

## Architecture

Producer → Kafka → Consumer → ClickHouse → Analytics Queries

- **Producer** generates API events and publishes them to Kafka
- **Kafka** acts as a durable, scalable message broker
- **Consumer** reads events, batches them, and inserts into ClickHouse
- **ClickHouse** stores events for fast analytical queries

---

## Tech Stack

- **Kafka** (Confluent Docker images)
- **ClickHouse** (MergeTree engine)
- **Python 3**
- **Docker Compose**

All components run locally with minimal resources.

---

## Data Model

Kafka event example:

```json
{
  "event_time": "2026-01-17T12:45:12",
  "user_id": "user_42",
  "endpoint": "/api/payments",
  "status_code": 200,
  "latency_ms": 124
}

