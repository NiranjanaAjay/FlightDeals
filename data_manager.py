# import os
# import requests
# from dotenv import load_dotenv
# from flight_data import FlightData
# from flight_search import FlightSearch
# from notification_manager import NotificationManager
#
# load_dotenv()
# flightData = FlightData()
# flightSearch = FlightSearch()
# notif_man = NotificationManager()
#
# class DataManager:
#     #This class is responsible for talking to the Google Sheet.
#     def __init__(self):
#         self.sheety_url = os.environ["SHEETY_URL"]
#
#         sheety_header = {
#             "Authorization": os.environ["SHEETY_PASS"]
#         }
#
#         self.response = requests.get(url=self.sheety_url,headers=sheety_header)
#         self.sheety_data = self.response.json()
#
#         print("DEBUG: Sheety data response:", self.sheety_data)
#
#         for i in self.sheety_data['prices']:
#             self.city_name = i['city']
#             self.price = i['lowestPrice']
#             iata_code = flightData.iata_code(self.city_name)
#
#             sheety_params = {
#                 "price":{
#                     "iataCode":iata_code
#                 }
#             }
#
#             requests.put(url=f"{self.sheety_url}/{i['id']}",json=sheety_params,headers=sheety_header)
#             price, departure_date = flightSearch.find_price(iata_code, flightData.auth_token)
#
#             if price:
#                 notif_man.send_msg(self.city_name,float(price),float(self.price),departure_date)

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ['SHEETY_URL']
SHEETY_EMAIL_ENDPOINT = os.environ['EMAIL_URL']

class DataManager:

    def __init__(self):
        self._user = os.environ["SHEETY_ID"]
        self._password = os.environ["SHEETY_PASS"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        print(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(response.text)

    def get_emails(self):
        emails=[]
        response = requests.get(url=SHEETY_EMAIL_ENDPOINT, auth=self._authorization)
        data = response.json()
        for i in data["users"]:
            user_email = i["whatIsYourEmail?"]
            emails.append(user_email)
        return emails