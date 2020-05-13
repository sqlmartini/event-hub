import time
import os
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

CONNECTION_STR = os.environ['EVENT_HUB_CONN_STR']
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

def create_json_message():
    message = {}
    message['RecordName'] = 'tag_' + str(random.randint(0, 300))
    message['DataSourceName'] = 'server_' + str(random.randint(0, 300))
    message['Ts'] = datetime.today().isoformat() ## current datetime in ISO format
    message['Value'] = random.uniform(0,300) ## random floating point between 0 and 300
    message['Quality'] = random.randrange(3) ## random number between 0 and 2
        
    message_payload = json.dumps(message)
    return message_payload


def send_event_data_batch(producer):
    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(create_json_message()))
    producer.send_batch(event_data_batch)

if __name__ == '__main__':
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )

    with producer:
        #while True:
        # Send 100 messages in a batch
        for x in range(99):
            send_event_data_batch(producer)
            
        # Wait 30 seconds and then run it again 
        #print('Waiting for 30 seconds until sending next batch')
        #time.sleep(30) 