import csv

import requests
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from accounts_manager.permissions import IsMerchant
from merchant import settings


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def export(request: HttpRequest) -> HttpResponse:
    data = request.GET.copy()
    data['phone'] = request.user.username
    data['merchant_id'] = request.user.merchant_id
    data['minAmount'] = data.get('f-Value-from-to', None).split('-')[0] if data.get('f-Value-from-to', None) else 0
    data['maxAmount'] = data.get('f-Value-from-to', None).split('-')[1] if data.get('f-Value-from-to', None) else None
    response = requests.get(f'{settings.AMAN_API_URL}export/', params=data, verify=False)
    content = response.json()
    if not content['responseCode'] == 200:
        return Response({"status": "failed", "message": "Something went wrong"}, status=400)

    data = content['responseData']
    # Generate the csv file and send it as response
    response = HttpResponse(content_type='text/csv')
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    response['Content-Disposition'] = 'attachment; filename="transactions-{}.csv".csv'.format(timestamp)
    writer = csv.writer(response)
    writer.writerow(['Date', 'transaction_id', 'Amount', 'Status', 'Type', 'terminal_id'])
    for transaction in data:
        writer.writerow(transaction.values())
    return response
