import os
import sys
import time
from json import loads
from kafka import  KafkaConsumer

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from common.util.context import Context
from common.util.logging import info_logger
from common.util.logging import error_logger
# from .common.util.context import Context
# from .common.util.logging import info_logger
# from .common.util.logging import error_logger

# ------------------------------------------#
# Loading Kafka Config File
# ------------------------------------------#
config_file = f'{script_dir}/config/kafka_consumer.yaml'
info_logger(config_file)
context = Context(config_file)


#-----------Consume records from a Kafka cluster.------------
#------------------------------------------------------------
class Consumer(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def run(self):
        # create an instance of the consumer with the configurations
        consumer = KafkaConsumer(self.config_file)

        
        # Subscribe to topic

        # Kafka_Topic="secedgartopic0"
        # consumer.subscribe([Kafka_Topic])
        consumer.subscribe([self.config_file['topics']])

        # Poll for new messages from Kafka and print them.
        try:
            while True:
                message = consumer.poll(1.0)
                if message is None:
                    info_logger("Waiting...")
                elif message.error():
                    error_logger("ERROR: %s".format(message.error()))
                else:
                    # Extract the (optional) key and value, and print.
                    info_logger("Consumed event from topic {topics}: key = {key} value = {value}".format(
                        topic=message.topics(), key=message.key().decode('utf-8'), value=message.value().decode('utf-8')))

        except KeyboardInterrupt:

            pass
        
        # Commit final offsets
        consumer.close()

if __name__ == "__main__":
    Consumer(context)

