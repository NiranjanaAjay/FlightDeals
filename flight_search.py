import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from flight_data import FlightData
from notification_manager import NotificationManager

load_dotenv()
notif_man = NotificationManager()
auth_token = FlightData().auth_token
initial = "LON"

flight_search_url = os.environ["FLIGHT_OFFERS_URL"]

flightData = FlightData()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def find_price(self,city_name):
        date = datetime.today().strftime("%Y-%m-%d")
        data = {
            "currencyCode": "GBP",
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": initial,
                    "destinationLocationCode": city_name.upper(),
                    "departureDateTimeRange": {
                        "date": date
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT"
                }
            ],
            "sources": ["GDS"]
        }

        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url=flight_search_url,json=data,headers=headers)
        result = response.json()
        try:
            offer = result['data'][0]
            price = offer['price']['total']
            notif_man.send_msg(price)

        except (KeyError, IndexError):
            print(f"{city_name.upper()}: No flight data available.")