from analytics.models import Terminal
from analytics.serializers import ChainSerializer
from analytics.models import Chain

class ChainServices:

    @staticmethod
    def create_Chain(chain,terminal_id):
        errors=[]

        chain['received_id']=chain['id']
        if not Chain.objects.filter(terminal_id__id=terminal_id,name=chain['name'],received_id=chain['received_id']).exists():
            chain['terminal_id']=terminal_id
            serializer =ChainSerializer(data=chain)

            if serializer.is_valid():
                serializer.save()
            else:
                errors.append( serializer.errors)

        if errors:
            return errors, False

        return 'Chain added successfully',  True