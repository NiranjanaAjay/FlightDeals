import os
import requests
from dotenv import load_dotenv
from flight_data import FlightData
from flight_search import FlightSearch

load_dotenv()
flightData = FlightData()
flightSearch = FlightSearch()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_url = os.environ["SHEETY_URL"]

        self.response = requests.get(url=self.sheety_url)
        self.sheety_data = self.response.json()

        for i in self.sheety_data['prices']:
            self.city_name = i['city']
            self.price = i['lowestPrice']
            iata_code = flightData.iata_code(self.city_name)

            sheety_params = {
                "price":{
                    "iataCode":iata_code
                }
            }
            requests.put(url=f"{self.sheety_url}/{i['id']}",json=sheety_params)
            flightSearch.find_price(iata_code)
