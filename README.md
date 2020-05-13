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
        | ---------- | ---------- |
        | CONNECTION_STR | Obtained from Shared Access Policy setting of Event Hub namespace
        | EVENTHUB_NAME | Name of your Azure Event Hub

        | ENV VAR NAME | VALUE |
        | ---------- | ---------- |
        | AZURE_CLIENT_ID | id of an Azure Active Directory application
        | AZURE_TENANT_ID | id of the application's Azure Active Directory tenant
        | AZURE_CLIENT_SECRET | one of the application's client secrets

## Python 3.7 Virtual Environment Creation and Configuration (Windows)
    ```
    python.exe -m venv venv
    venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install azure-eventhub
    ```