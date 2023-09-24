import logging
import threading
from typing import Any
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
from singleton_factory import SingletonMeta

from variables import variables

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        
    else:
        logging.error("Connection failed with code", rc)

def on_message(client, userdata, message: MQTTMessage):
    # message.payload
    pass

def on_publish(client, userdata, mid):
    logging.info(f"Publish: ${mid}")

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected from MQTT broker")
    pass

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect

class ConnectionFactory(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._task = threading.Thread(target=self._run_task)
        self.stopping = threading.Event()

    def start(self):
        try:
            self._task.start()
        except KeyboardInterrupt:
            logging.info("Closing connection due to close app")

    def stop(self):
        logging.info("Closing connection")
        self.stopping.set()
        client.disconnect()

    def _run_task(self):
        logging.info("Starting connection")
        status = client.connect(host = variables.mq_host())
        logging.info("connection statis is: " + str(status))
        client.loop_forever()
    
    def send_message(self, topic: str, payload):
        logging.info(f"Publish to topic: {topic} message: {payload}")
        try:
            client.publish(topic=topic, payload=payload)
        except BaseException as e:
            logging.error(f"Error during publishing message to the topic: {topic}", e)

connection_factory = ConnectionFactory()