from analytics.models import Transactions,CustomerDetails
from analytics.serializers import TerminalSerializer,CustomerDetailsSerializer,TransactionsSerializer
from .pos_services import POSServices
from accounts_manager.services.account import AccountServices
from datetime import datetime
import pytz


class TransactionServices:


    @staticmethod
    def set_settlement(data):
        errors=[]
        total_number_transactions= len(data['transaction_ids'])
        if Transactions.objects.filter(aman_batch_id=data['aman_batch_id'],batch_id=data['batch_id'],is_void=False).count() != total_number_transactions:
            return 'total number of transactions doesn\'t equal save transactions' , False
        for transaction_id in data['transaction_ids']:
            if Transactions.objects.filter(aman_batch_id=data['aman_batch_id'],batch_id=data['batch_id'],stan=transaction_id,is_void=False).exists():
                transaction = Transactions.objects.get(aman_batch_id=data['aman_batch_id'],batch_id=data['batch_id'],stan=transaction_id,is_void=False)
                transaction.is_settled=True
                transaction.save()
            else:
                errors.append(transaction_id)

        if errors:
            return errors, False
        else:
            return {'message': 'success'}, True
    

    @staticmethod
    def save_transaction_data(data):
        errors=[]
        for item in data:
            try:
                user=item['merchant']
                date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
                user['date']=date
                serializer=None
                merchant_data,merchant_data_success = AccountServices.save_user_with_pos(data=user)

                if(not merchant_data_success):
                    errors.append(merchant_data)
                    continue

                bank_details_data,bank_details_data_success = AccountServices.create_bank_details(bank_details=item['bank_details'],user_id=merchant_data['id'])
                if(not bank_details_data_success):
                    errors.append(bank_details_data)
                    continue

                pos=item['pos']
                pos['date']=date
                pos_data,pos_data_success = POSServices.create_POS(pos=pos,user_id=merchant_data['id'])
                if(not pos_data_success):
                    errors.append(pos_data) 
                    continue

                transaction=item['transaction']
                status=transaction.get('status','create')
                transaction['terminal_id']=pos_data['id']
                if status == 'create':
                    serializer=TransactionsSerializer(data=transaction)

                elif status == 'update':
                    if (Transactions.objects.filter(terminal_id__id=pos_data['id'],rrn=transaction['rrn'],stan=transaction['stan'],auth_id=transaction['auth_id']).exists()):
                        pos_transaction=Transactions.objects.filter(terminal_id__id=pos_data['id'],rrn=transaction['rrn'],stan=transaction['stan'],auth_id=transaction['auth_id']).last()
                        if date > pos_transaction.date :
                            serializer=TransactionsSerializer(pos_transaction,data=transaction,partial=True)
                    else:
                        serializer=TransactionsSerializer(data=transaction)
                
                    
                if serializer.is_valid():
                    serializer.save()

                else:
                    errors.append(serializer.errors)
                    continue


                
                customer_details_data,customer_details_data_success = TransactionServices.create_customer_details(customer_details=item['customer_details'],transaction_id=(serializer.data)['id'])
                if(not customer_details_data_success):
                    errors.append(customer_details_data)
                    continue

            except Exception as e:
                errors.append(e)


        if errors:
            return errors, False

        return 'POS transactions added successfully', True


    @staticmethod
    def create_customer_details(customer_details,transaction_id):
        errors=[]
        transaction=Transactions.objects.get(id=transaction_id)

        if not CustomerDetails.objects.filter(transaction_id=transaction,issuer=customer_details['issuer'],pan=customer_details['pan']
        ,card_holder_name=customer_details['card_holder_name']).exists():
        
            customer_details['transaction_id']=transaction_id
            serializer =CustomerDetailsSerializer(data=customer_details)

            if serializer.is_valid():
                serializer.save()
            else:
                errors.append( serializer.errors)

        if errors:
            return errors, False

        return 'Customer details added successfully',  True

