import requests
from django.http import HttpRequest
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts_manager.permissions import IsMerchant
from merchant import settings


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='POSId',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='POS ID',
            required=False
        ),
    ],
    responses={
        200: openapi.Response(
            description='OK',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='status'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='message'),
                    'statistics': openapi.Schema(type=openapi.TYPE_OBJECT, description='statistics', properties={
                        'today': openapi.Schema(type=openapi.TYPE_OBJECT, description='today'),
                        'current-week': openapi.Schema(type=openapi.TYPE_OBJECT, description='current-week'),
                        'last-week': openapi.Schema(type=openapi.TYPE_OBJECT, description='last-week'),
                        'current-month': openapi.Schema(type=openapi.TYPE_OBJECT, description='current-month'),
                        'last-month': openapi.Schema(type=openapi.TYPE_OBJECT, description='last-month'),
                        'last-quarter': openapi.Schema(type=openapi.TYPE_OBJECT, description='last-quarter'),
                    }),
                }
            )
        ),
    }
)
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def pos_statistics(request: HttpRequest) -> Response:
    phone_number = request.user.username
    pos = request.GET.get('pos', None)
    response = requests.get(f'{settings.AMAN_API_URL}PosStatistics/', params={'Phone': phone_number, 'pos': pos, 'merchant_id': request.user.merchant_id}, verify=False)
    # print("pos statistics" , response, response.json())
    content = response.json()
    if content['responseCode'] == 200:
        statistics = content['responseData']
        return Response({"status": "success", "message": "POS statistics", "statistics": statistics}, status=200)
    else:
        return Response({"status": "failed", "message": "Something went wrong"}, status=400)
