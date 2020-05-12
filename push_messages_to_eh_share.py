import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from datetime import datetime
import json
import random
import time
import urllib
import hmac
import hashlib
import base64
import requests

## Script Variables
connection_string = '' #'Endpoint=sb://<youreventhubnamespace>.servicebus.windows.net/;SharedAccessKeyName=etcetc.'
sb_name = '' #EH namespace
eh_name = '' #EH name
sas_name = '' #SAS token name
sas_value = '' #SAS Key 


def get_auth_token(sb_name, eh_name, sas_name, sas_value):
    """
    Returns an authorization token dictionary 
    for making calls to Event Hubs REST API.
    """
    uri = urllib.parse.quote_plus("https://{}.servicebus.windows.net/{}" \
                                  .format(sb_name, eh_name))
    sas = sas_value.encode('utf-8')
    expiry = str(int(time.time() + 31536000)) #expire in a year
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
    return  {"sb_name": sb_name,
             "eh_name": eh_name,
             "token":'SharedAccessSignature sr={}&sig={}&se={}&skn={}' \
                     .format(uri, signature, expiry, sas_name)
            }

def create_json_record():
    bot_dict = {}
    bot_dict['StandardBotTransactionReport'] = {}
    bot_dict['StandardBotTransactionReport']['botid'] = random.choice([12345, 67891, 88888])
    bot_dict['StandardBotTransactionReport']['bot_transaction_timestamp'] = str(datetime.now())
    bot_dict['StandardBotTransactionReport']['success'] = random.choice([True, False]) ## Randomly choose true or false. 
    bot_dict['StandardBotTransactionReport']['elapsed_time_sec'] = random.randint(0,300) ## random amount of time btween 1 and 300 seconds
    bot_dict['BotSpecificTransactionData'] = {}
    bot_dict['BotSpecificTransactionData']["ColumnA"] = "A"
    bot_dict['BotSpecificTransactionData']["ColumnB"] = "B"
    bot_dict['BotSpecificTransactionData']["ColumnC"] = "C"
        
    message_payload = json.dumps(bot_dict)
    return message_payload

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
 	    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_string)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(create_json_record()))
        event_data_batch.add(EventData(create_json_record()))
        event_data_batch.add(EventData(create_json_record()))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)


### Get Ready to Run the code
auth_token = get_auth_token(sb_name, eh_name, sas_name, sas_value)

url = f'https://{sb_name}.servicebus.windows.net/{eh_name}/messages?timeout=60&api-version=2014-01'

headers = {
    "Authorization": auth_token['token'],
    "Content-Type": "application/atom+xml;type=entry;charset=utf-8",
    "Host": f"{sb_name}.servicebus.windows.net"  
}

while True:     
    res = requests.post(url=url, headers=headers, json=create_json_record())
    print(f"{res} - pausing for 10 seconds")
    print(f"{res.text}")
    time.sleep(1) # wait 10 seconds and then run it again 

