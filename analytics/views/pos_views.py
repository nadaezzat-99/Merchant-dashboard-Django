from django.utils.datetime_safe import date
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse, HttpRequest
from rest_framework.permissions import IsAuthenticated

from accounts_manager.permissions import IsVendor
from analytics.services.pos_services import POSServices


@api_view(["DELETE"])
def deletePosView(request):
    data,success = POSServices.delete_POS(pos=request.data)
    if(not success):
        return JsonResponse({"error":data},status=400) 

    return JsonResponse(data, safe=False,status=200)