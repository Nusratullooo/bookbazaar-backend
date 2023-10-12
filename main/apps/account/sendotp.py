import random
from ..account.models.user import User

from twilio.rest import Client as TwilioClient
from rest_framework.response import Response

from django.core.mail import EmailMessage
from django.conf import settings

import json
import random

import requests
from pprint import pprint
from eskiz.client import SMSClient


from datetime import datetime, timedelta



# account_sid = 'AC59d0629692bb9a29e294b73663696933'
# auth_token = "9a1035b65c166d343605b2697a80b10b"
# twilio_phone = "+18329798435"
# client = TwilioClient(account_sid, auth_token)


# def send_sms_code(username):
#     user_phone_number = User.objects.get(username=username).username
#     otp = random.randint(100000, 999999)
#     user_otp = User.objects.get(username=username)
#     user_otp.otp = otp
#     user_otp.save()
#     client.messages.create(
#                      body="Your verification code for Liber is " + str(otp),
#                      from_=twilio_phone,
#                      to=user_phone_number
#                  )
#     return Response(status=200)



def send_password_as_sms(username):
    user_phone_number = User.objects.get(username=username).username
    otp = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    user_otp.otp = otp
    user_otp.save()
    client = SMSClient(
        api_url = "https://notify.eskiz.uz/api/",
        email = "burixonzoda.nusratullo@gmail.com",
        password = "i3wlzbBJ5FnVtO6itVUYVGMCo6cbHJM5Jk3v7ciF"
    )
    resp = client._send_sms(
        phone_number=str(user_phone_number),
        message=f"Your otp is {otp}"
    )
    print(resp)

# def send_password_as_sms(username):
#     user_phone_number = User.objects.get(username=username).username
#     otp = random.randint(100000, 999999)
#     user_otp = User.objects.get(username=username)
#     user_otp.otp = otp
#     user_otp.save()
#     from_whom = '+998901234567'
#     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjUsImlzcyI6Imh0dHA6Ly9ub3RpZnkuZXNraXoudXovYXBpL2F1dGgvbG9naW4iLCJpYXQiOjE1NDc1Njc1NTAsImV4cCI6MTU0NzY1Mzk1MCwibmJmIjoxNTQ3NTY3NTUwLCJqdGkiOiJTSmxYYUFSU3FPS29ZWUlxIn0.O2B_87_KlmGwPqXZfaISy5VPT6N2_QpjN3h7lGlvpDo'
#     payload = {
#             "mobile_phone": str(user_phone_number),
#             "message": 'message',
#             "from_whom": from_whom,
#             "callback_url": 'http://0000.uz/test.php'
#         }
#     response = requests.post("/message/sms/send", token=token, payload=payload)
#     return response

    # url = "https://notify.eskiz.uz/api/message/sms/send" + "?token=" + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjUsImlzcyI6Imh0dHA6Ly9ub3RpZnkuZXNraXoudXovYXBpL2F1dGgvbG9naW4iLCJpYXQiOjE1NDc1Njc1NTAsImV4cCI6MTU0NzY1Mzk1MCwibmJmIjoxNTQ3NTY3NTUwLCJqdGkiOiJTSmxYYUFSU3FPS29ZWUlxIn0.O2B_87_KlmGwPqXZfaISy5VPT6N2_QpjN3h7lGlvpDo"
    # status = "good job"
    # data = {
    #         'mobile_phone': user_phone_number,
    #         'message': "Test",
    #         'from': "4546",
    #         'callback_url': "http://0000.uz/test.php"
    #     }
    # print(data)
    # data = {
    #     "message": {"recipients": [str(user_phone_number)]},
    #     "priority": "default",
    #     "sms": {"content": f"your password for liber system is: {otp}"},
    # }

    # requests.post(url, data=json.dumps(data), timeout=5)

# from shared import rdb
# send_sms_api = "https://notify.eskiz.uz/api/message/sms/send"

# def send_password_as_sms(data):
#     # while not rdb.get('eskiz_token'):
#     #     get_token_eskiz()

#     headers = {
#         "Authorization": "Bearer " + rdb.get('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjUsImlzcyI6Imh0dHA6Ly9ub3RpZnkuZXNraXoudXovYXBpL2F1dGgvbG9naW4iLCJpYXQiOjE1NDc1Njc1NTAsImV4cCI6MTU0NzY1Mzk1MCwibmJmIjoxNTQ3NTY3NTUwLCJqdGkiOiJTSmxYYUFSU3FPS29ZWUlxIn0.O2B_87_KlmGwPqXZfaISy5VPT6N2_QpjN3h7lGlvpDo')
#     }

#     return requests.post(
#         send_sms_api,
#         data=data,
#         headers=headers
#     )



def password_reset_verification_code_by_phone_number(username):
    # user_phone_number = User.objects.get(username=username).username
    # otp = random.randint(100000, 999999)
    # user_otp = User.objects.get(username=username)
    # user_otp.otp = otp
    # user_otp.save()

    user_phone_number = User.objects.get(username=username).username
    resetting_code = random.randint(100000, 999999)
    user_activating_code = User.objects.get(username=username)
    time = datetime.now() + timedelta(minutes=1)
    user_activating_code.expiration_time_reset = time.strftime('%H:%M:%S')
    user_activating_code.activating_code = resetting_code
    user_activating_code.save()

    client = SMSClient(
        # email = "test@eskiz.uz",
        # password = "j6DWtQjjpLDNjWEk74Sx"
        api_url = "https://notify.eskiz.uz/api/",
        email = "burixonzoda.nusratullo@gmail.com",
        password = "i3wlzbBJ5FnVtO6itVUYVGMCo6cbHJM5Jk3v7ciF"
    )
    resp = client._send_sms(
        phone_number=str(user_phone_number),
        message=f"Your confrim code is {resetting_code}" 
    )
    print(resp)
    return Response(status=200)


def send_otp_to_email(username):
    user_email = User.objects.get(username=username).username
    otp = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    user_otp.otp = otp
    user_otp.save()

    email = EmailMessage(
        'LiberUz',
        f'LiberUz uchun tasdiqlash kodi: {otp}',
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.send()

    return Response(status=200)


def password_reset_verification_code_by_email(username):
    user_email = User.objects.get(username=username).username
    verification_code = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    time = datetime.now() + timedelta(minutes=3)
    user_otp.expiration_time_reset = time.strftime('%H:%M:%S')
    user_otp.activating_code = verification_code
    user_otp.save()

    email = EmailMessage(
        'LiberUz',
        f'LiberUz uchun tasdiqlash kodi: {verification_code}',
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.send()

    return Response(status=200)




