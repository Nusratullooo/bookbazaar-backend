from django.contrib.auth import get_user_model
from rest_framework import generics, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

from ..utils import generate_random_password
from ...common import permissions
from ..serializers import user as user_serializer_
# from ..utils import generate_random_password, send_password_as_sms

from ...account.sendotp import (
    # send_sms_code, 
    send_password_as_sms,
    password_reset_verification_code_by_phone_number,
    send_otp_to_email,
    password_reset_verification_code_by_email
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.generics import GenericAPIView
from django.utils.translation import ugettext_lazy as _

from main.apps.account import serializers

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = user_serializer_.MyTokenObtainPairSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = user_serializer_.UserSerializer
    queryset = User.objects.filter(is_virified=True).exclude(is_staff=True, is_superuser=True)
    search_fields = ["username", "user_generate_id"]


user_list_view = UserListAPIView.as_view()


class UserGeneratePasswordAPIView(APIView):
    serializer_class = user_serializer_.UserPhoneNumberSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        password = generate_random_password()
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        phone_number = data.validated_data.get("phone_number")
        user_obj = User.objects.filter(phone_number=phone_number)
        if user_obj.exists():
            user_obj = user_obj.first()
            user_obj.set_password(password)
            user_obj.save()
        else:
            User.objects.create_user(
                phone_number=phone_number,
                password=password,
            )

        send_password_as_sms(phone_number)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "your password has been sent to your phone number",
            },
        )


user_generate_password_view = UserGeneratePasswordAPIView.as_view()


class UserObtainTokenAPIView(ObtainAuthToken):
    serializer_class = user_serializer_.AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = user_serializer_.UserSerializer(instance=user)
        details = user_serializer.data
        details.update(token=token.key)
        return Response(details)


user_login_view = UserObtainTokenAPIView.as_view()


class LogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"message": "You have successfully logged out"},
        )


user_logout_view = LogoutAPIView.as_view()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter_details()
    serializer_class = user_serializer_.UserDetailSerializer
    lookup_field = "guid"


user_detail_api_view = UserDetailAPIView.as_view()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializer_.UserUpdateSerializer
    permission_classes = [permissions.UpdatePermission]
    lookup_field = "guid"


user_update_api_view = UserUpdateAPIView.as_view()


class AuthUserRegistrationView(generics.GenericAPIView):
    serializer_class = user_serializer_.UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            if "998" in serializer.data['username']:
                send_password_as_sms(serializer.data['username'])
            elif "@" in serializer.data['username']:
                send_otp_to_email(serializer.data['username'])
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered',
                'user': serializer.data
            }

            return Response(response, status=status_code)


user_registration_api_view = AuthUserRegistrationView.as_view()


class ResendOtpToPhoneNumberAPIView(generics.GenericAPIView):
    serializer_class = user_serializer_.UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        try:
            user = User.objects.get(username=username)
            # if "998" in data['username']:
            #     send_sms_code(data['username'])
            # elif "@" in data['username']:
            #     send_otp_to_email(data['username'])
            if "998" in data['username']:
                send_password_as_sms(data['username'])
            elif "@" in data['username']:
                send_otp_to_email(data['username'])
        except User.DoesNotExist:
            return Response('User does not exits')
        return Response('OTP resent successfully')


user_resend_otp_api_view = ResendOtpToPhoneNumberAPIView.as_view()


class AuthUserLoginView(generics.GenericAPIView):
    serializer_class = user_serializer_.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'phone_number': serializer.data['phone_number'],
                }
            }

            return Response(response, status=status_code)


user_login_api_view = AuthUserLoginView.as_view()


class VerifyPhoneOTP(generics.GenericAPIView):
    serializer_class = user_serializer_.VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            otp = serializer.data['otp']
            users = User.objects.filter(username=username)
            for user in users:
                if user.otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong otp'
                    })
                dates = str(datetime.now().strftime('%H:%M:%S'))
                users_date = str(user.expiration_time_register)
                if users_date < dates:
                    return Response({
                        'status': 400,
                        'message': "Code vaqti tugagan, qayta code jo'nating!",
                    })
                else:
                    user.is_virified = True
                    user.save()

                    return Response({
                        'status': 200,
                        'message': 'Account virified'
                    })
            return Response({
                'status': 400,
                'message': 'Bunday account mavjud emas!'
            })
        else:
            return Response({
                'status': 400,
                'message': 'Bunday account mavjud emas!'
            })


user_otp_verify_api_view = VerifyPhoneOTP.as_view()


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = user_serializer_.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        data = request.data
        username = data['username']

        if valid:
            serializer.save()
            try:
                user = User.objects.get(username=username)
                if "998" in serializer.data['username']:
                    password_reset_verification_code_by_phone_number(serializer.data['username'])
                elif "@" in serializer.data['username']:
                    password_reset_verification_code_by_email(serializer.data['username'])
                status_code = status.HTTP_201_CREATED
            except User.DoesNotExist:
                return Response({'status': 'error', 'message': 'User does not exits'},
                                status=status.HTTP_400_BAD_REQUEST)
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Code successfully sent',
                'user': serializer.data
            }
            return Response(response, status=status_code)


password_reset_api_view = PasswordResetAPIView.as_view()


class PasswordResetCodeCheckView(generics.GenericAPIView):
    serializer_class = user_serializer_.PasswordResetCodeCheckSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        dates = str(datetime.now().strftime('%H:%M:%S'))
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        if valid:
            try:
                user = User.objects.get(activating_code=serializer.data['confirm_code'])
                if user.expiration_time_reset < dates:
                    return Response({
                        'status': 400,
                        'message': "Code vaqti tugagan, qayta code jo'nating!",
                    })
                else:
                    return Response({'status': 'success', 'message': "Code tastiqlandi!"}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'error', 'message': "Sizga xozir jo'natilgan code ni kiriting!"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': "Serializer not valid!!"}, status=status.HTTP_400_BAD_REQUEST)


password_reset_check_view = PasswordResetCodeCheckView.as_view()


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Accepts the following POST parameters: email,  password1, password2
    Returns the success/fail message.
    """
    serializer_class = user_serializer_.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        data = request.data
        username = data['username']

        if serializer.is_valid(raise_exception=False):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response('User does not exits')
            if serializer.data['new_password1'] != serializer.data['new_password2']:
                return Response({'status': False, 'message': "two fields should be the same!"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                UserModel = get_user_model()
                user = UserModel.objects.get(username=serializer.data['username'])
                user.password = make_password(serializer.data['new_password1'])
                user.save()
                return Response({"message": "Password successfully updated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'status': False, 'message': 'The entered password is incorrect', 'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


password_reset_confirm_view = PasswordResetConfirmView.as_view()


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = user_serializer_.PasswordChangeSerializer

    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            if serializer.data['new_password1'] != serializer.data['new_password2']:
                return Response({'status': 'error', 'message': _("PThese two fields should be the same!")},
                                status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['new_password1'])
                user.save()
                return Response({"message": _("Password successfully updated")}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': _('Password is incorrect')},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'status': 'error', 'message': _('This phone number does not exist'), 'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


password_change_view = PasswordChangeView.as_view()
