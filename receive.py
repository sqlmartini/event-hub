import os
import json
import logging
from azure.eventhub import EventHubConsumerClient

# Script Variables
CONNECTION_STR = os.environ['EVENT_HUB_CONN_STR']
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']
consumer_group = '$Default'

def on_event(partition_context, event):
    partition_context.update_checkpoint(event)
    print(event)

if __name__ == '__main__':
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME,
        consumer_group=consumer_group,
    )

    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )

    except KeyboardInterrupt:
        print('Stopped receiving.')