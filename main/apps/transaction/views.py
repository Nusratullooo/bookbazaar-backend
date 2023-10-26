from django.conf import settings
from paycomuz import Paycom
from paycomuz.views import MerchantAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from clickuz.views import ClickUzMerchantAPIView
from . import serializers
from .helper import CheckPayMeTransaction
from .helper import CheckClickTransaction
from .models import TRANSACTIONTYPECHOICES, Transaction, TRANSACTIONSTATUS
from .service import initialize_transaction
# from .helper import CheckTransaction
from .models import TRANSACTIONTYPECHOICES
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from clickuz import ClickUz



from rest_framework_simplejwt import authentication
# from rest_framework import permissions

converter_amount = settings.PAYME_PRICE_HELPER
converter_amount_click = settings.CLICK_PRICE_HELPER


class InitializePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = serializers.InitializePaymentSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        transaction_type = data.validated_data.get("transaction_type")
        price = data.validated_data.get("price")

        transaction_id = initialize_transaction(
            request.user,
            price,
            transaction_type,
        )
        generated_link = ""
        if transaction_type == TRANSACTIONTYPECHOICES.PAYME:
            """
            Note:
            PayMe accepts price in UZB TIYN that's why, we multiply the price by 100 # noqa
            sum = 10 000
            Payme accepts it as 10000 tiyns that is 100 sums
            thats why we send 10000 sums * 100 that is 1 000 000 tiyn
            """
            price = price * converter_amount
            # TODO: change success return url
            generated_link = Paycom().create_initialization(
                price,
                transaction_id,
                return_url="fa05-82-215-106-101.ngrok-free.app/api-auth/login",
            )
        elif transaction_type == TRANSACTIONTYPECHOICES.CLICK:
            price = price * converter_amount_click
            generated_link = ClickUz.generate_url(
                order_id=transaction_id,
                amount=price,
                return_url="https://fa05-82-215-106-101.ngrok-free.app/login",
                )
        return Response(
            status=status.HTTP_200_OK,
            data={"generated_link": generated_link},
        )


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptPaymeRequestsView(MerchantAPIView):
    VALIDATE_CLASS = CheckPayMeTransaction


accept_payme_request_view = AcceptPaymeRequestsView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionListSerializer
    filter_fields = ["transaction_type", "status"]


transaction_list_api_view = TransactionListAPIView.as_view()
