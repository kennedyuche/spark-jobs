import os
import sys
import time
from time import sleep
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import KafkaError
from functools import reduce
from kafka_consumer import Consumer
from kafka_producer import Producer


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
config_file = f'{script_dir}/config/kafka_main.yaml'
info_logger(config_file)
context = Context(config_file)


class run(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def run_client(self):
        try:
            admin = KafkaAdminClient(self.config_file['bootstrap_servers'])

            new_topics = [NewTopic(topic, self.config_file['num_partitions'], self.config_file['replication_facrtor']) 
                        for topic in self.config_file['topics']]
            # Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.

            # Call create_topics to asynchronously create topics. A dict
            # of <topic,future> is returned.
            fs = admin.create_topics(new_topics, validate_only=False)

            # Wait for each operation to finish.
            for topic, f in fs.items():
                try:
                    f.result()  # The result itself is None
                    info_logger("Topic {} created".format(topic))
                except Exception as e:
                    error_logger("Failed to create topic {}: {}".format(topic, e))
            
        except Exception:
            pass

        tasks = [
                Producer(), Consumer()
        ]

        for t in tasks:
            t.start()

        time.sleep(10)


if __name__ == "__main__":
    run(Context)