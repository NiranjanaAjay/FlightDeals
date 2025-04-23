import requests
import os
from dotenv import load_dotenv

load_dotenv()
amadeus_url = os.environ["AMADEUS_URL"]
amadeus_api_key = os.environ["AMADEUS_API_KEY"]
amadeus_secret = os.environ["AMADEUS_API_SECRET"]
amadeus_auth_url = os.environ["AUTH_URL"]

class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self):
        self.auth_token = self.get_auth()

    def iata_code(self, city_name):
        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }
        amadeus_params = {
            "keyword":city_name.upper()
        }
        response = requests.get(url=amadeus_url,params=amadeus_params, headers=headers)
        return response.json()['data'][0]['iataCode']

    def get_auth(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        amadeus_data = {
            "grant_type": "client_credentials",
            "client_id": amadeus_api_key,
            "client_secret": amadeus_secret
        }
        token_value = requests.post(url=amadeus_auth_url, headers = header, data = amadeus_data)
        return token_value.json()['access_token']

