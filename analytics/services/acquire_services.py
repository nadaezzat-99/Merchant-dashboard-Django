from analytics.models import Terminal
from analytics.serializers import AcquireSerializer
from analytics.models import Acquire

class AcquireServices:

    @staticmethod
    def create_Acquire(acquire,terminal_id):
        errors=[]

        for item in acquire:
            item['received_id']=item['id']
            if not Acquire.objects.filter(terminal_id__id=terminal_id,name=item['name'],received_id=item['received_id']).exists():

                item['terminal_id']=terminal_id
                serializer =AcquireSerializer(data=item)

                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append( serializer.errors)
        
        if errors:
            return errors, False

        return 'Acquire added successfully',  False