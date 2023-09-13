from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from accounts_manager.views import checkPhoneNumber, checkOTP, Login, ChangePassword, resetPassword,saveAccountWithPOSView,forgetPassword

check_phone_number = swagger_auto_schema(
    method='post',
    operation_description='Check if phone number is valid',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
        }),
    responses={200: openapi.Response("Create reading lesson successfully")}
)(checkPhoneNumber)


check_otp = swagger_auto_schema(
    method='post',
    operation_description='Check if OTP is valid',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP'),
        }),
    responses={200: openapi.Response("Create reading lesson successfully")}
)(checkOTP)


register = swagger_auto_schema(
    method='post',
    operation_description='Register a new user',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm password'),
        }),
    responses={200: openapi.Response("Password reset successfully")}
)(resetPassword)


forgetPassword = swagger_auto_schema(
    method='post',
    operation_description='Forget password api',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm password'),
        }),
    responses={200: openapi.Response("Password reset successfully")}
)(forgetPassword)

login = swagger_auto_schema(
    method='post',
    operation_description='Login a user',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }),
    responses={200: openapi.Response("Create reading lesson successfully")}
)(Login)


forget_password = swagger_auto_schema(
    method='post',
    operation_description='Forget password',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='old password'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm password'),
        }),
    responses={200: openapi.Response("Password changed successfully")}
)(ChangePassword)


saveAccountWithPOS = swagger_auto_schema(
    method='post',
    operation_description='Save users with pos',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='user name'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='user phone number'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email of the user'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='date of creation from aman side'),
            "pos":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'merchant_id': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'terminal_id': openapi.Schema(type=openapi.TYPE_STRING, description='terminal id'),
                        'serial_number': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'vendor_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'terminal_type_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'address': openapi.Schema(type=openapi.TYPE_STRING, description='address of the user'),
                        'acquire': openapi.Schema(type=openapi.TYPE_ARRAY,
                         items=openapi.Items(type=openapi.TYPE_OBJECT,properties={
                            "id":openapi.Schema(type=openapi.TYPE_STRING, description='acquire id'),
                            "name":openapi.Schema(type=openapi.TYPE_STRING, description='acquire name'),
                            })
                        ,description='array of acquire objects'),
                        "chain":openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                                'id': openapi.Schema(type=openapi.TYPE_STRING, description='chain id'),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='chain name'),
                            },description='chain object'),

                    }
                
            ),
        "bank_details":openapi.Schema(type=openapi.TYPE_ARRAY,
                         items=openapi.Items(type=openapi.TYPE_OBJECT,properties={
                            'bank_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                            'bank_branch': openapi.Schema(type=openapi.TYPE_STRING, description='bank branch'),
                            'account_number': openapi.Schema(type=openapi.TYPE_STRING, description='account number'),
                            })),
        }),
    responses={200: openapi.Response("Merchants added successfully")}
)(saveAccountWithPOSView)



