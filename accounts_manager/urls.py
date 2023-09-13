from django.urls import path, include

from accounts_manager.swagger import *
from accounts_manager.views import checkPhoneNumber, checkOTP, Logout, Login, resetPassword, saveAccountWithPOSView, \
    getData, forgetPassword, get_pos

app_name = 'accounts_manager'

apis = [
    ## login with phone and password and return token
    path('login', Login, name='login'),

    ## logout and delete the user_token
    path('logout', Logout, name='logout'),

    # endpoint take phone_number and check if this phone in merchant data
    path('phoneCheck', checkPhoneNumber, name='phone_check'),
    # if True
    path('checkOTP', checkOTP, name='check_otp'), # [+]
    # if True
    ## take a new password, confirm_pass and create new user
    ## or change password if forget_password
    path('resetPassword', resetPassword, name='register'),
    path('forgetPassword', forgetPassword, name='forgetPassword'),


    path('changePassword', ChangePassword, name='change_password'), # [+]

    path('save_user_pos', saveAccountWithPOSView, name='save_users_pos'), # [+]

    path('getData', getData, name="getData"),

    path('get_pos', get_pos, name="get_pos"),


]

urlpatterns = [
    path('/auth/', include(apis)),
]
