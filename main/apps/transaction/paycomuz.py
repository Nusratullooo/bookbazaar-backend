from django.conf import settings
import base64
from decimal import Decimal

assert settings.PAYCOM_SETTINGS.get('KASSA_ID') != None
assert settings.PAYCOM_SETTINGS.get('ACCOUNTS') != None
assert settings.PAYCOM_SETTINGS['ACCOUNTS'].get('KEY') != None

TOKEN = settings.PAYCOM_SETTINGS['TOKEN']
KEY = settings.PAYCOM_SETTINGS['ACCOUNTS']['KEY']


class PayComResponse(object):
    # LINK = 'https://checkout.paycom.uz'
    # LINK = 'https://checkout.test.paycom.uz'
    LINK = 'https://test.paycom.uz'

    def create_initialization(self, amount: Decimal, order_id: str, return_url: str) -> str:
        """

        documentation : https://help.paycom.uz/ru/initsializatsiya-platezhey/otpravka-cheka-po-metodu-get

        # >>> self.create_initialization(amount=Decimal(1), order_id='1', return_url='https://fa05-82-215-106-101.ngrok-free.app/api/v1/transaction/integration_with_payme/success/')
        """

        params = f"m={TOKEN};ac.{KEY}={order_id};a={amount};c={return_url}"
        encode_params = base64.b64encode(params.encode("utf-8"))
        encode_params = str(encode_params, 'utf-8')
        url = f"{self.LINK}/{encode_params}"
        return url
# https://checkout.paycom.uz/bT02MjI1ZWQ0YzA2Njk4MTY5Yzg3ZGFiMWY7YWMub3JkZXJfaWQ9MjthPTE1MDAwLjAwO2M9aHR0cHM6Ly9leGFtcGxlLmNvbQ==

# https://checkout.paycom.uz/bT02MjI5ZWM2MTRmZWQxNTJhMTA2ODAwMmE7YWMub3JkZXJfaWQ9MjU3O2E9MTAwMDAwLjAwO2M9aHR0cHM6Ly9leGFtcGxlLmNvbQ==