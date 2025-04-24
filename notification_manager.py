import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
origin = "LONDON"

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        pass

    def send_msg(self,leastprice,userprice, city_name):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        city = city_name.upper()
        user_price = userprice
        least_price = leastprice

        if least_price < user_price:
            msg = f"{city} from {origin} is in your budget, it is {least_price}"

            message = client.messages.create(
                body=msg,
                from_="+17542871306",
                to= os.environ["PHNO"],
            )