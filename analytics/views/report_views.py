import requests
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts_manager.permissions import IsMerchant
from merchant import settings
from rest_framework.permissions import IsAuthenticated


@swagger_auto_schema(
    method='get',
    manual_parameters = [
        openapi.Parameter(
            name='POS',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='POS ID',
            required=False
        ),
        openapi.Parameter(
            name='dateFrom',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            name='dateTo',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            name='TimeFrameId',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False
        ),
    ],
    responses={
        200: openapi.Response(
            description='OK',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_OBJECT, description='count data', properties={
                        'points': openapi.Schema(type=openapi.TYPE_ARRAY, description='points', items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'time': openapi.Schema(type=openapi.TYPE_STRING, description='2023-01-04T04:00:00.000003'),
                            'value': openapi.Schema(type=openapi.TYPE_INTEGER, description='value'),
                        })),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description='total'),
                        'ratio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ratio'),
                    }),
                    'avg': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
                        'points': openapi.Schema(type=openapi.TYPE_ARRAY, description='points', items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'time': openapi.Schema(type=openapi.TYPE_STRING, description='2023-01-04T04:00:00.000003'),
                            'value': openapi.Schema(type=openapi.TYPE_INTEGER, description='value'),
                        })),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description='total'),
                        'ratio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ratio'),
                    }),
                    'sum': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
                        'points': openapi.Schema(type=openapi.TYPE_ARRAY, description='points', items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'time': openapi.Schema(type=openapi.TYPE_STRING, description='2023-01-04T04:00:00.000003'),
                            'value': openapi.Schema(type=openapi.TYPE_INTEGER, description='value'),
                        })),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description='total'),
                        'ratio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ratio'),
                    }),
                    'sum_card_info': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
                        'points': openapi.Schema(type=openapi.TYPE_ARRAY, description='points',
                                                 items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                     'time': openapi.Schema(type=openapi.TYPE_STRING,
                                                                            description='2023-01-04T04:00:00.000003'),
                                                     'value': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                             description='value'),
                                                 })),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description='total'),
                        'ratio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ratio'),
                    }),
                    'category_card': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
                        'all': openapi.Schema(type=openapi.TYPE_INTEGER, description='points'),
                        'sale': openapi.Schema(type=openapi.TYPE_INTEGER, description='points'),
                        'refund': openapi.Schema(type=openapi.TYPE_INTEGER, description='points'),
                        'installment': openapi.Schema(type=openapi.TYPE_INTEGER, description='points'),
                        'void': openapi.Schema(type=openapi.TYPE_INTEGER, description='points'),
                    }),
                }
            )
        ),
    }
)
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def report(request):
    data = request.GET.copy()
    data['phone'] = request.user.username
    data['merchant_id'] = request.user.merchant_id
    data['minAmount'] = data.get('f-Value-from-to', None).split('-')[0] if data.get('f-Value-from-to', None) else 0
    data['maxAmount'] = data.get('f-Value-from-to', None).split('-')[1] if data.get('f-Value-from-to', None) else None
    print("REPORT DATA => ", data)
    response = requests.get(f'{settings.AMAN_API_URL}report/', params=data, verify=False)
    content = response.json()
    print(content)
    print("REPORT RESPONSE CONTENT => ", content)
    if not content['responseCode'] == 200:
        return Response({'message': "Something went wrong", 'response': content}, status=status.HTTP_400_BAD_REQUEST)
    return Response(content['responseData'], status=status.HTTP_200_OK)

