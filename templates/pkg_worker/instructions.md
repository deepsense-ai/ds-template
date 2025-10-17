# Worker Package Usage

This package provides a **background worker** that supports multiple worker types: **Celery** (default), **Cron**, or **Kafka**. The template comes pre-configured with Celery, but you can easily adapt it for other worker types.

## Key Features

- **Multiple Worker Types**: Support for Celery, Cron, and Kafka workers
- **Task Management**: Structured task definition and execution
- **Configuration**: Environment-based worker configuration
- **Docker Ready**: Pre-configured for containerized deployment
- **Monitoring**: Built-in health checks and structured logging

## Worker Types

### 1. Celery Worker (Default Implementation)

**Pre-configured with Redis backend and Celery Beat scheduler.**

#### Basic Task Definition
```python
from celery import Celery
from .tasks import process_data_task

app = Celery('worker')

@app.task
def process_data_task(data):
    \"\"\"Process data asynchronously.\"\"\"
    # Your processing logic here
    return result
```

#### Advanced Task with Retry
```python
@celery_app.task(bind=True, max_retries=3)
def process_item(self, item_id: int, item_data: dict):
    try:
        # Your processing logic here
        return {"status": "processed", "item_id": item_id}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

#### Running Celery Worker
```bash
# Start Celery worker
uv run celery -A packages.<worker_package>.worker worker --loglevel=info

# Start Celery Beat (scheduler)
uv run celery -A packages.<worker_package>.worker beat --loglevel=info

# Start both worker and beat
uv run celery -A packages.<worker_package>.worker worker --beat --loglevel=info
```

### 2. Cron Worker

**For simple scheduled tasks using Python's schedule library.**

#### Implementation
```python
# Add to pyproject.toml dependencies:
# "schedule>=1.2.0"

import schedule
import time
from .tasks import scheduled_task

def run_scheduler():
    \"\"\"Run the cron scheduler.\"\"\"
    # Schedule tasks
    schedule.every(10).minutes.do(scheduled_task)
    schedule.every().hour.do(another_task)
    schedule.every().day.at("02:00").do(daily_cleanup)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
```

#### Running Cron Worker
```bash
uv run python packages/<worker_package>/src/<package_name>/worker.py
```

### 3. Kafka Worker

**For event-driven processing using Apache Kafka.**

#### Implementation
```python
# Add to pyproject.toml dependencies:
# "kafka-python>=2.0.2"

from kafka import KafkaConsumer
from .tasks import process_message

def run_kafka_consumer():
    \"\"\"Run the Kafka consumer.\"\"\"
    consumer = KafkaConsumer(
        'my-topic',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        try:
            process_message(message.value)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

if __name__ == "__main__":
    run_kafka_consumer()
```

#### Running Kafka Worker
```bash
uv run python packages/<worker_package>/src/<package_name>/worker.py
```

## Configuration

### Worker Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    worker_type: str = "celery"  # celery, cron, or kafka
    
    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Kafka Configuration
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "my-topic"
    
    # General Configuration
    worker_concurrency: int = 4
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Environment Variables
```bash
# Worker Type
WORKER_TYPE=celery  # or cron, kafka

# Celery (if using celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Kafka (if using kafka)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=my-topic

# General
WORKER_CONCURRENCY=4
LOG_LEVEL=INFO
```

## Switching Worker Types

### 1. Update Dependencies
```toml
# For Cron Worker
dependencies = [
    "schedule>=1.2.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

# For Kafka Worker  
dependencies = [
    "kafka-python>=2.0.2",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]
```

### 2. Modify worker.py
```python
from .config import settings

if settings.worker_type == "celery":
    from .celery_worker import run_celery_worker
    run_celery_worker()
elif settings.worker_type == "cron":
    from .cron_worker import run_cron_worker
    run_cron_worker()
elif settings.worker_type == "kafka":
    from .kafka_worker import run_kafka_worker
    run_kafka_worker()
```

## Production (Docker)

```bash
# Build and run worker container
docker build -t packages/<worker_package> .
docker run -d --name worker packages/<worker_package>
```

## Development
- Main worker logic in `worker.py`
- Task definitions in `tasks.py`
- Configuration in `config.py`
- Choose the appropriate worker type for your use case
- Implement proper error handling and retry logic
- Monitor worker health and performance