from datetime import datetime
import pytz
import requests

from accounts_manager.models import Account,BankDetails
from accounts_manager.serializers import AccountCreateUpdateSerializer,BankDetailsSerializer
from analytics.services.pos_services import POSServices
from merchant import settings


class AccountServices:
    @staticmethod
    def save_user(data):
        errors = []
        for item in data:
            account = AccountCreateUpdateSerializer(item)

            if account.is_valid():
                account.save()

            else:
                error = {item['merchant_id']: account.errors}
                errors.append(error)

        if errors:
            return errors, False

        return 'User added successfully', True

    @staticmethod
    def save_user_with_pos(data):
        errors = []
        try:
            data['username'] = data.pop('phone')
            if Account.objects.filter(username=data['username']).exists():
                # print("####1")
                account = Account.objects.get(username=data['username'])
                if not isinstance(data['date'], datetime):
                    data_time = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
                else:
                    data_time=data['date']
                if data_time > account.date:   
                    account_serializer = AccountCreateUpdateSerializer(
                        account, data=data, partial=True)
                else:
                    return {data['username']: 'The sent date is too old' }, False

            else:
                account_serializer = AccountCreateUpdateSerializer(data=data)
                    
                
            if account_serializer.is_valid():
                account_serializer.save()
                # print("#####4", account_serializer)
            else:
                # print("#####5", account_serializer.errors)
                error = {data['username']: account_serializer.errors}
                errors.append(error)

            if 'bank_details' in data and data['bank_details']:        

                bank_details_data,bank_details_data_success = AccountServices.create_bank_details(bank_details=data['bank_details'],user_id=(account_serializer.data)['id'])
                if(not bank_details_data_success):
                    errors.append(bank_details_data)

            if 'pos' in data and  data['pos']:
                pos_data=data['pos']
                pos_data['date']=data['date']
                save_pos, status = POSServices.create_POS(pos=pos_data,user_id=(account_serializer.data)['id'])

                if not status:
                    errors.append(save_pos)
        except Exception as e:
            return {'error':str(e)}, False
        if errors:
            return errors, False

        return account_serializer.data, True


    @staticmethod
    def getData(user):
        if user:
            serializer = AccountCreateUpdateSerializer(user, context={'fields':('name', 'username', 'pos')})
            return serializer.data, True
        return None, True

    @staticmethod
    def create_bank_details(bank_details,user_id):
        errors=[]
        user=Account.objects.get(id=user_id)
        if type(bank_details) is list:
            for detail in bank_details:
                if not BankDetails.objects.filter(user_id=user,bank_name=detail['bank_name'],bank_branch=detail['bank_branch']
                ,account_number=detail['account_number']).exists():
                    
                    detail['user_id']=user_id
                    serializer =BankDetailsSerializer(data=detail)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        errors.append( serializer.errors)
        else:
            if not BankDetails.objects.filter(user_id=user,bank_name=bank_details['bank_name'],bank_branch=bank_details['bank_branch']
                ,account_number=bank_details['account_number']).exists():
                    
                    bank_details['user_id']=user_id
                    serializer =BankDetailsSerializer(data=bank_details)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        errors.append( serializer.errors)



        if errors:
            return errors, False

        return 'Bank details added successfully',  True

    @staticmethod
    def get_pos(phone_number: str, merchant_id: int) -> (dict, bool):
        try:
            response = requests.get(f'{settings.AMAN_API_URL}POSs/', params={'phone': phone_number, 'merchant_id': merchant_id}, verify=False)
            content = response.json()
            if content['responseCode'] == 200:
                return content['responseData'], True
            return {'error': 'Something went wrong'}, False
        except Exception as e:
            return {'error': str(e)}, False

    @staticmethod
    def has_pos(phone_number: int) -> bool:
        response = requests.get(f'{settings.AMAN_API_URL}check/', params={'phone_number': phone_number}, verify=False)
        content = response.json()
        if not content['responseCode'] == 200:
            return False
        return content['responseData']['hasPOSs']

