from django.utils.datetime_safe import date
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse, HttpRequest
from rest_framework.permissions import IsAuthenticated

from accounts_manager.permissions import IsVendor
from analytics.services.transaction_services import TransactionServices


@api_view(["POST"])
def savePOSTransactionDataView(request):
    input=request.data
    
    transactions_data,success = TransactionServices.save_transaction_data(data=input)
    if(not success):
        return JsonResponse({"error":transactions_data}, safe=False,status=400) 
    
    return JsonResponse(transactions_data, safe=False,status=200)


@api_view(["POST"])
def setSettlementView(request):
    data,success = TransactionServices.set_settlement(data=request.data)
    print("#########4")

    if(not success):
        return JsonResponse({"error":data}, safe=False,status=400)

    return JsonResponse(data, safe=False,status=200)
