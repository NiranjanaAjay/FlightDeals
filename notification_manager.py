import os
from dotenv import load_dotenv
from twilio.rest import Client
from data_manager import DataManager

load_dotenv()
datamanager = DataManager()
origin = "LONDON"

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        pass

    def send_msg(self,price):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        city = datamanager.city_name.upper()
        user_price = datamanager.price
        least_price = price

        if least_price < user_price:
            MESSAGE = f"{city} from {origin} is in your budget, it is {least_price}"

            message = client.messages.create(
                body=MESSAGE,
                from_="+17542871306",
                to= os.environ["PHNO"],
            )