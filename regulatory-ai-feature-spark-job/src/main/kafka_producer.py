import os
import sys
import time
from json import dumps
from kafka import KafkaProducer

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
# sys.path.append(os.path.dirname(script_dir))

# from .common.util.context import Context
# from .common.util.logging import info_logger
from common.util.context import Context
from common.util.logging import info_logger

# ------------------------------------------#
# Loading Kafka Config File
# ------------------------------------------#
config_file = f'{script_dir}/config/kafka_producer.yaml'
info_logger(config_file)
context = Context(config_file)


#-----------Produce records to a Kafka cluster.------------
#------------------------------------------------------------
class Producer(object):
    def __init__(self, config_file):
        self.config_file = config_file
    
    def run(self):
        # create an instance of the producer with the configurations
        producer = KafkaProducer(self.config_file)

        topic_list = self.config_file['topics']
        kf_connectors = list(map(lambda x: producer(x), topic_list))

        # Example code
        producer.send(kf_connectors, b'test message for kafka!!')
        producer.send(kf_connectors, key=b'message-two', value=b'This is Kafka-Python')
        producer.flush()
        time.sleep(1)

        # topic
        # Kafka_Topic="secedgartopic0"
        
        # # publish message to topic (asynchronous)
        # producer.send(topic_list, b'test message for kafka!!')
        # producer.send(topic_list, key=b'message-two', value=b'This is Kafka-Python')
        # producer.flush()
        # time.sleep(1)
            
if __name__ == "__main__":
    Producer(context)