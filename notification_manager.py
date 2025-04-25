# import os
# from dotenv import load_dotenv
# from twilio.rest import Client
#
# load_dotenv()
# origin = "LONDON"
#
# class NotificationManager:
#     #This class is responsible for sending notifications with the deal flight details.
#     def __init__(self):
#         pass
#
#     def send_msg(self,city_name, least_price, user_price, depart_date):
#
#         if least_price < user_price:
#             account_sid = os.environ["TWILIO_ACCOUNT_SID"]
#             auth_token = os.environ["TWILIO_AUTH_TOKEN"]
#             client = Client(account_sid, auth_token)
#             city = city_name.upper()
#             date = depart_date
#
#             msg = f"GREAT DEALS AVAILABLE!!\n {origin} to {city} for ₹{least_price} on {date}"
#
#             message = client.messages.create(
#                 body=msg,
#                 from_="+17542871306",
#                 to= os.environ["PHNO"],
#             )

import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

class NotificationManager:

    def __init__(self):
        self.client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ["TWILIO_AUTH_TOKEN"])

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            body=message_body,
            to=os.environ["TWILIO_VIRTUAL_NUMBER"]
        )
        print(message.sid)

    def send_msg(self, message_body):
        message = self.client.messages.create(
                            body=message_body,
                            from_="+17542871306",
                            to= os.environ["PHNO"],
                        )
        print(message.sid)