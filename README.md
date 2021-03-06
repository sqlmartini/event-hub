# event-hub

This is a simple repo to show how to send and receive messages using Azure Event Hub.

- **send.py**:  Sends a batch of 100 messages of mocked up time-series machine telemetry
- **receive.py**:  Receives and prints messages from the Event Hub

Azure Event Hubs client library for Python Samples:
https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/eventhub/azure-eventhub/samples

# Requirements:
- Python 3.7
- Azure Event Hubs client library for Python (https://pypi.org/project/azure-eventhub/)
- Two environment variables configured:

    | ENV VAR NAME | VALUE |
    |--------------|-------|
    | CONNECTION_STR | Obtained from Shared Access Policy setting of Event Hub namespace |
    | EVENTHUB_NAME | Name of your Azure Event Hub |