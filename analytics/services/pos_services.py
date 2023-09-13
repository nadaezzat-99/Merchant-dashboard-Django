from accounts_manager.models import Account
from analytics.models import Terminal,Transactions
from analytics.serializers import TerminalSerializer
from datetime import datetime
import pytz
from .acquire_services import AcquireServices
from .chain_services import ChainServices

class POSServices:


    @staticmethod
    def create_POS(pos,user_id):
        user=Account.objects.get(id=user_id)
        errors=[]
        
        pos['user_id']=user_id
        
        if not isinstance(pos['date'], datetime):
            data_time = datetime.strptime(pos['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
        else:
            data_time=pos['date']

        serializer=None

        if Terminal.objects.filter(merchant_id=pos['merchant_id'],terminal_id=pos['terminal_id']).exists():
            terminal=Terminal.objects.filter(merchant_id=pos['merchant_id'],terminal_id=pos['terminal_id']).last()
            terminal_id=terminal.id
            if terminal.date < data_time:

                saved_phone_number=terminal.user_id.username
                
                if (saved_phone_number != user.username):
                    old_user=terminal.user_id
                    terminal.user_id=user
                    terminal.save()
                    if Terminal.objects.filter(user_id=old_user,deactivated=False).count() == 0:
                        old_user.is_active=False
                        old_user.save()

                    moved_transactions=Transactions.objects.filter(terminal_id__user_id=old_user)
                    for item in moved_transactions:
                        item.user_id=user
                        item.save()
                
                else:
                    serializer=TerminalSerializer(instance=terminal,data=pos,partial=True)


        elif Terminal.objects.filter(terminal_id=pos['terminal_id']).exists():
            terminal=Terminal.objects.filter(terminal_id=pos['terminal_id']).last()
            terminal_id=terminal.id
            if terminal.date < data_time:
                old_merchant_id=terminal.merchant_id
                old_user=terminal.user_id
                old_username=terminal.user_id.username

                if(old_merchant_id != pos['merchant_id'] and old_username!= user.username ):
                    terminal.deactivated=True
                    terminal.save()
                    if Terminal.objects.filter(user_id=old_user,deactivated=False).count() == 0:
                        old_user.is_active=False
                        old_user.save()
                    serializer=TerminalSerializer(data=pos)


        else:
            serializer=TerminalSerializer(data=pos)

        if serializer:
            if serializer.is_valid():
                serializer.save()
                terminal_id=(serializer.data)['id']
                
            else:
                error = serializer.errors
                errors.append(error)
            
        if errors :
            return errors, False


        #add acquire
        if pos['acquire']:
            acquire_serializer, status = AcquireServices.create_Acquire(acquire=pos['acquire'],terminal_id=terminal_id)
            
            if not acquire_serializer:
                error = acquire_serializer
                errors.append(error)
                return errors, False
        
        if pos['chain']:
            chain_serializer, status = ChainServices.create_Chain(chain=pos['chain'],terminal_id=terminal_id)
            
            if not chain_serializer:
                error = chain_serializer
                errors.append(error)
                return errors, False
        

        if not serializer:
            return TerminalSerializer(instance=terminal).data, True
        else:
            return serializer.data, True

    @staticmethod
    def delete_POS(pos):
        if Terminal.objects.filter(merchant_id=pos['merchant_id'],terminal_id=pos['terminal_id'],user_id__username=pos['phone']).exists():
            terminal=Terminal.objects.filter(merchant_id=pos['merchant_id'],terminal_id=pos['terminal_id'],user_id__username=pos['phone']).last()
            user=terminal.user_id
            data_time = datetime.strptime(pos['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
            if data_time > terminal.date: 
                terminal.deleted=pos['deleted']
                terminal.deactivated=pos['deactivated']
                terminal.save()

                if Terminal.objects.filter(user_id=user,deactivated=False).count() == 0:
                    user.is_active=False
                    user.save()

            return 'success', True
        else:
            return 'No such terminal', False

    