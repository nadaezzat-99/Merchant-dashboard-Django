import random
import hashlib
import hmac
import base64
from rest_framework import status

import requests as requests
from django.http import JsonResponse, HttpRequest
# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts_manager.authentication.token_authentication import Token
from accounts_manager.models import Account, Otp
from accounts_manager.permissions import IsVendor, IsMerchant
from accounts_manager.serializers.account_serializer import AccountSerializer
from accounts_manager.services.account import AccountServices
from merchant import settings


@api_view(['POST',])
def Login(request):
    data = request.data
    phone_number = data['phone_number']
    response = requests.get(f'{settings.AMAN_API_URL}merchant/check?phone={phone_number}', verify=False)
    content = response.json()
    if not content['responseCode'] == 200:
        return Response({"message": "User does not exist", "status_code": 400}, status=400)
    has_pos = content['responseData']['hasPOSs']
    if Account.objects.filter(username=data['phone_number']).exists()and has_pos :
        user = Account.objects.get(username=data['phone_number'])
        user.has_pos = has_pos
        user.save()
    else:
        return Response({"message": "User does not exist", "status_code": 400}, status=400)
    if not user.check_password(data['password']):
        return Response({"message": 'Password mismatch', "status_code": 400}, status=400)

    serializer = AccountSerializer(user).data
    data = {'data': serializer}
    return Response(data, status=200)



@api_view(['POST',])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        user = request.user
        key = request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(user=user, key=key)
        token.delete()
        return Response({'status_code':200}, status=200)
    except Exception as e:
        return Response({'status_code':400}, status=400)


@api_view(["POST"])
def checkPhoneNumber(request):
    phone_number = request.data.get('phone_number')
    register = request.data.get('register', False)
    response = requests.get(f'{settings.AMAN_API_URL}merchant/check?phone={phone_number}', verify=False)
    content = response.json()
    # content = {
    #     "responseCode": 200,
    #     "responseDescription": "success",
    #     "responseData": {
    #         "merchantName": "Marwa Youssef",
    #         "mobileNumber": "01068368337",
    #         "hasPOSs": True,
    #         "merchant_id": "92276"
    #     }
    # }
    if register:
        if Account.objects.filter(username=phone_number).exists():
            account = Account.objects.get(username=phone_number)
            if content['responseCode'] == 200 and content['responseData']['hasPOSs'] and int(account.merchant_id) == int(content['responseData']['merchant_id']):
                return Response({'message': "This Merchant Already Registered."}, status=400)
            elif content['responseCode'] != 200:
                return Response({'message': "This Merchant Not Exist For Aman."}, status=400)
            elif content['responseCode'] == 200 and content['responseData']['hasPOSs'] and account.merchant_id != content['responseData']['merchant_id']:
                account.merchant_id = content['responseData']['merchant_id']
                account.name = content['responseData']['merchantName']
                account.has_pos = content['responseData']['hasPOSs']
                account.save()
        else: 
            if content['responseCode'] == 200 and content['responseData']['hasPOSs']:
                if Account.objects.filter(merchant_id=content['responseData']['merchant_id']).exists():
                    account = Account.objects.get(merchant_id=content['responseData']['merchant_id'])
                    account.username = content['responseData']['mobileNumber']
                    account.name = content['responseData']['merchantName']
                    account.has_pos = content['responseData']['hasPOSs']
                    account.save()
                else:
                    account = Account.objects.create(name=content['responseData']['merchantName'], merchant_id=content['responseData']['merchant_id'], username=content['responseData']['mobileNumber'], has_pos=content['responseData']['hasPOSs'])
                    account.set_unusable_password()
                    account.save()
            else:
                return Response({'message': "This Merchant Not Exist For Aman."}, status=400)                

    else:
        if Account.objects.filter(username=phone_number).exists():
            account = Account.objects.get(username=phone_number)
            print(content['responseCode'] == 200 and content['responseData']['hasPOSs'] and int(account.merchant_id) == int(content['responseData']['merchant_id']))
            if not (content['responseCode'] == 200 and content['responseData']['hasPOSs'] and int(account.merchant_id) == int(content['responseData']['merchant_id'])):
                return Response({'message': 'Phone Number Not Exist.'}, status=400)
        else:
            return Response({'message': 'Phone Number Not Registered.'}, status=400)

    generated_otp = random.randint(99999, 999999)
    Otp.objects.create(phone_number=phone_number, otp=generated_otp)
    message_text = "Your Verification Code is {}".format(generated_otp)

    API_SECRET = settings.SMS_SECRET_KEY
    message = "AccountId={}&Password={}&SenderName={}&ReceiverMSISDN={}&SMSText={}".format(settings.SMS_ACCOUNT_ID, settings.SMS_API_PASSWORD, settings.SMS_SENDER_NAME, phone_number, message_text)
    signature = hmac.new(bytes(API_SECRET, 'latin-1'), msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest().upper()
    url = "https://41.78.23.43/web2sms?bridgeEndpoint=true&httpClient.cookiePolicy=ignoreCookies"
    data = """<?xml version="1.0" encoding="UTF-8"?><SubmitSMSRequest xmlns="http://www.edafa.com/web2sms/sms/model/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.edafa.com/web2sms/sms/model/" SMSAPI.xsd="" xsi:type="SubmitSMSRequest"><AccountId>{}</AccountId><Password>{}</Password><SecureHash>{}</SecureHash><SMSList><SenderName>{}</SenderName><ReceiverMSISDN>{}</ReceiverMSISDN><SMSText>{}</SMSText></SMSList></SubmitSMSRequest>""".format(settings.SMS_ACCOUNT_ID, settings.SMS_API_PASSWORD, signature, settings.SMS_SENDER_NAME, phone_number, message_text)
    headers = {
        'Content-Type': "application/xml",
    }
    response = requests.request("POST", url, data=data, headers=headers, verify=False)
    if response.status_code != 200:
        return Response({'message': "Something Went Wrong While Sending Otp."}, status=400)
    return Response({'message': "Otp Sent."}, status=200)
    



@api_view(["POST"])
def checkOTP(request):
    otp = request.data.get('otp')
    phone_number = request.data.get('phone_number')
    if not Otp.objects.filter(phone_number=phone_number, verified=False, used=False).exists():
        return Response({"status": "failed", "message": "OTP is not valid"}, status=400)
    otp_object = Otp.objects.filter(phone_number=phone_number, verified=False, used=False).order_by('created_at').last()
    # print(otp_object.created_at + timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME), timezone.now())
    if otp_object.created_at + timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME) < timezone.now():
        return Response({"status": "failed", "message": "OTP is expired"}, status=400)
    if otp_object.otp == otp:
        otp_object.verified = True
        otp_object.save()
        return Response({"status": "success", "message": "OTP is valid"}, status=200)
    else:
        return Response({"status": "failed", "message": "OTP is not valid"}, status=400)

@api_view(["POST"])
def resetPassword(request):
    data = request.data
    register = False
    if not Account.objects.filter(username=data['phone_number']).exists():
        return Response({"status": "failed", "message": "User does not exist"}, status=404)
    if not Otp.objects.filter(phone_number=data['phone_number'], verified=True, used=False).exists():
        return Response({"status": "failed", "message": "Your OTP has expired. Please try again"}, status=400)
    otp_object = Otp.objects.filter(phone_number=data["phone_number"], verified=True, used=False).order_by('created_at').last()
    if otp_object.created_at + timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME) < timezone.now():
        return Response({"status": "failed", "message": "OTP is expired"}, status=400)
    if not otp_object.verified:
        return Response({"status": "failed", "message": "verify your otp first"}, status=400)
    if not data['password'] == data['confirm_password']:
        return Response({"status": "failed", "message": "password mismatch"}, status=400)
    if Account.objects.filter(username=data['phone_number']).exists():
        user = Account.objects.get(username=data['phone_number'])
        if user.force_password_change_on_first_time:
            user.force_password_change_on_first_time = False
            register = True
        user.set_password(data['password'])
        user.save()
        serializer = AccountSerializer(user).data
        otp_object.used = True
        otp_object.save()
        return Response({"status": "success", "message": "password reset successfully", "register": register, "data": serializer}, status=200)
    else:
        return Response({"status": "failed", "message": "phone number is not registered"}, status=400)

@api_view(["POST"])
def ChangePassword(request):
    data = request.data
    if not request.user.is_authenticated:
        return Response({"status": "failed", "message": "User is not authenticated"}, status=400)
    user = request.user
    if not user.check_password(data['old_password']):
        return Response({"status": "failed", "message": "old password is not valid"}, status=400)
    if data['password'] == data['confirm_password']:
        user.set_password(data['password'])
        user.save()
        return Response({"status": "success", "message": "password changed"}, status=200)
    else:
        return Response({"status": "failed", "message": "password mismatch"}, status=400)


@api_view(["POST"])
def forgetPassword(request):
    data = request.data
    if not Account.objects.filter(username=data['phone_number']).exists():
        return Response({"status": "failed", "message": "User does not exist"}, status=404)
    if not Otp.objects.filter(phone_number=data['phone_number'], verified=True, used=False).exists():
        return Response({"status": "failed", "message": "Your OTP has expired. Please try again"}, status=400)
    otp_object = Otp.objects.filter(phone_number=data["phone_number"], verified=True, used=False).order_by('created_at').last()
    if otp_object.created_at + timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME) < timezone.now():
        return Response({"status": "failed", "message": "OTP is expired"}, status=400)
    if not otp_object.verified:
        return Response({"status": "failed", "message": "verify your otp first"}, status=400)
    if not data['password'] == data['confirm_password']:
        return Response({"status": "failed", "message": "password mismatch"}, status=400)
    if Account.objects.filter(username=data['phone_number']).exists():
        user = Account.objects.get(username=data['phone_number'])
        if user.force_password_change_on_first_time:
            user.force_password_change_on_first_time = False
        user.set_password(data['password'])
        user.save()
        otp_object.used = True
        otp_object.save()
        return Response({"status": "success", "message": "password reset successfully"}, status=200)
    else:
        return Response({"status": "failed", "message": "phone number is not registered"}, status=400)


@api_view(["POST"])
def saveAccountWithPOSView(request):

    data,success = AccountServices.save_user_with_pos(data=request.data)
    if(not success):
        return JsonResponse({"error":data}, safe=False,status=400) 

    return JsonResponse(data, safe=False,status=200)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def getData(request):
    data, success = AccountServices.getData(user=request.user)
    if not success:
        return JsonResponse({"error":data},status=400)
    return JsonResponse(data, safe=False, status=200)

@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_pos(request: HttpRequest) -> Response:
    data, success = AccountServices.get_pos(phone_number=request.user.username, merchant_id=request.user.merchant_id)
    if not success:
        return Response(data, status=400)
    return Response(data, status=200)

@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def test_token(request: HttpRequest) -> Response:
    return Response({'data': 'Success'}, status=200)
