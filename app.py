import connexion
import requests
import json
from connexion import NoContent
from pykafka import KafkaClient
import datetime
import yaml
from flask_cors import CORS, cross_origin
import logging.config

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


def report_goals_scored(goal):
    try:
        client = KafkaClient(hosts="{}:{}".format(app_config["kafka"]["domain"], app_config["kafka"]["port"]))
        topic = client.topics[app_config["kafka"]["topic"]]

        producer = topic.get_sync_producer()
        msg = {
            "type": "goals_scored",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": goal
        }
        msg_str = json.dumps(msg)
        producer.produce(msg_str.encode('utf-8'))

        logger.info("Goal scored reported successfully: {}".format(goal))
    except:
        logger.error("Service error while storing the goal scored")

    return NoContent, 201


def report_cards_received(card):
    try:
        client = KafkaClient(hosts="{}:{}".format(app_config["kafka"]["domain"], app_config["kafka"]["port"]))
        topic = client.topics[app_config["kafka"]["topic"]]

        producer = topic.get_sync_producer()
        msg = {
            "type": "cards_received",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": card
        }
        msg_str = json.dumps(msg)
        producer.produce(msg_str.encode('utf-8'))

        logger.info("Card received reported successfully: {}".format(card))
    except:
        logger.error("Service error while storing the card received")

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)