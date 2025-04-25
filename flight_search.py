# import os
# from dotenv import load_dotenv
# import requests
# from datetime import datetime, timedelta
#
# load_dotenv()
# initial = "LON"
#
# flight_search_url = os.environ["FLIGHT_OFFERS_URL"]
#
#
# class FlightSearch:
#     #This class is responsible for talking to the Flight Search API.
#     def __init__(self):
#         self.date_from = datetime.today() + timedelta(days=1)
#
#     def find_price(self,city_name, auth_token):
#         data = {
#             "currencyCode": "GBP",
#             "originDestinations": [
#                 {
#                     "id": "1",
#                     "originLocationCode": initial,
#                     "destinationLocationCode": city_name.upper(),
#                     "departure": {
#                         "date": self.date_from
#                     }
#                 }
#             ],
#             "travelers": [
#                 {
#                     "id": "1",
#                     "travelerType": "ADULT"
#                 }
#             ],
#             "sources": ["GDS"]
#         }
#
#         headers = {
#             'Authorization': f'Bearer {auth_token}',
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.post(url=flight_search_url,json=data,headers=headers)
#         result = response.json()
#
#         try:
#             offer = result['data'][0]
#             price = offer['price']['total']
#             departure_datetime = offer['itineraries'][0]['segments'][0]['departure']['at']
#             departure_date = departure_datetime.split("T")[0]
#             return price, departure_date
#
#         except (KeyError, IndexError):
#             print(f"{city_name.upper()}: No flight data available.")
#             current_date += timedelta(days=1)
#
#         return None, None

import requests
import os
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:

    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        return response.json()