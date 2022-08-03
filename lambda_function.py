import json
import os
import logging
from botocore.vendored import requests

# Initializing a logger and settign it to INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Reading environment variables and generating a Telegram Bot API URL
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)

# Helper function to prettify the message if it's in JSON
def process_message(input):
    try:
        raw_json = json.loads(input)
        output = json.dumps(raw_json, indent=4)
        output = output.strip('"')
    except:
        output = input

    return output


def lambda_handler(event, context):
    
    # logging the event for debugging
    logger.info("### EVENT DETAIL ###")
    logger.info(json.dumps(event))

    # Reading the message "Message" field from the SNS message
    records = event['Records'];
    for record in records:
        message = ''
        if record['EventSource'] == 'aws:sns':
            message = process_message(record['Sns']['Message'])
        else:
            message = process_message(record['Message'])

        # Payload to be set via POST method to Telegram Bot API
        payload = {
            "text": message.encode("utf8"),
            "chat_id": CHAT_ID,
            "parse_mode": "markdown"
        }
        requests.post(TELEGRAM_URL, payload)

