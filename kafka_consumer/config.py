import os
import json
import logging
import logging.config

from dotenv import load_dotenv

load_dotenv()

CONSUMER_ID = os.getenv("CONSUMER_ID")
ENV = os.getenv("ENV", "development").lower()

KAFKA_CONSUMER_LOGGING_CONFIG = (
    "kafka_consumer/logging_config.prod.json"
    if ENV == "production"
    else "kafka_consumer/logging_config.dev.json"
)


def init_logging():
    with open(KAFKA_CONSUMER_LOGGING_CONFIG, "r") as f:
        config = json.load(f)
    for handler in config.get("handlers", {}).values():
        filename = handler.get("filename")
        if filename:
            filename = filename.format(CONSUMER_ID=CONSUMER_ID)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            handler["filename"] = filename
    logging.config.dictConfig(config)