# import requests
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# amadeus_url = os.environ["AMADEUS_URL"]
# amadeus_api_key = os.environ["AMADEUS_API_KEY"]
# amadeus_secret = os.environ["AMADEUS_API_SECRET"]
# amadeus_auth_url = os.environ["AUTH_URL"]
#
# class FlightData:
#     #This class is responsible for structuring the flight data.
#     def __init__(self):
#         self.auth_token = self.get_auth()
#
#     def iata_code(self, city_name):
#         headers = {
#             "Authorization": f"Bearer {self.auth_token}"
#         }
#         amadeus_params = {
#             "keyword":city_name.upper()
#         }
#         response = requests.get(url=amadeus_url,params=amadeus_params, headers=headers)
#         return response.json()['data'][0]['iataCode']
#
#     def get_auth(self):
#         header = {
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#         amadeus_data = {
#             "grant_type": "client_credentials",
#             "client_id": amadeus_api_key,
#             "client_secret": amadeus_secret
#         }
#         token_value = requests.post(url=amadeus_auth_url, headers = header, data = amadeus_data)
#         return token_value.json()['access_token']
#

class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data):
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight

