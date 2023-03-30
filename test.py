import os
import django
from os import getenv
from dotenv import load_dotenv
import datetime
load_dotenv()
from redis import Redis
# from telegram import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# from apps.telegram_bot.models import *


# from lib.trading_platforms_api.__init__ import *

# api = Binance(api_key = getenv("BINANCE_API_KEY"), api_secret=getenv("BINANCE_SECRET_KEY"))
# symbol = "ETHUSDT"
# # print(api.get_current_currency(sybmol=symbol))

# klines = api.get_klines(symbol=symbol, interval="1m", limit=1000)

# for kline in klines:
#     print(datetime.datetime.fromtimestamp(kline[0]/1000).strftime('%Y-%m-%d %H:%M:%S'))


import requests
import json

conn = requests.session()

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_USERNAME = "fluxadmin"
INFLUXDB_PASSWORD = "fluxpassword"
INFLUXDB_ORG = "org_test"
INFLUXDB_ORG_ID = "org_test_id"

auth_url = f"{INFLUXDB_URL}/api/v2/signin"
response = conn.post(auth_url, auth=(INFLUXDB_USERNAME, INFLUXDB_PASSWORD))
session_token = response.headers["influxdb-oss-session"]

# Create a new token
token_url = f"{INFLUXDB_URL}/api/v2/authorizations"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {conn.cookies['influxdb-oss-session']}",
}

data = {
    "orgID": INFLUXDB_ORG_ID,
    "description": "Your token description",
    "permissions": [
        {
            "action": "read",
            "resource": {
                "type": "buckets",
                "orgID": INFLUXDB_ORG_ID
            }
        },
        {
            "action": "write",
            "resource": {
                "type": "buckets",
                "orgID": INFLUXDB_ORG_ID
            }
        },
        # Add more permissions as needed
    ],
}

response = requests.post(token_url, headers=headers, data=json.dumps(data))

from dotenv import load_dotenv
load_dotenv()
import influxdb_client

client = influxdb_client.InfluxDBClient(
    url="http://localhost:8086/",
    token="B1C1cZWdpcSPsDWuy5EMP-RuUuq3-2q7UFWdZC38sbv5kWOH0_PXFPWtXZel4aBwygTKJkrCrRCnRgGE5WDFzA===",
    org="org_test"
)



# print(databases)
