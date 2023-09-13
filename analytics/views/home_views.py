import requests
from django.db.models import Sum, Avg
from django.http import HttpRequest
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import datetime

from accounts_manager.permissions import IsMerchant
from analytics.services.char_services import ChartServices
from merchant import settings
from rest_framework.permissions import IsAuthenticated


@swagger_auto_schema(
    method='get',
    manual_parameters=[
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
                    'avg': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
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
                    'sum': openapi.Schema(type=openapi.TYPE_OBJECT, description='status', properties={
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
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def home(request: HttpRequest) -> Response:
    data = request.GET.copy()
    data['Phone'] = request.user.username
    data['merchant_id'] = request.user.merchant_id
    time_frame = request.GET.get("TimeFrameId", None)
    date_from = request.GET.get("dateFrom", None)
    date_to = request.GET.get("dateTo", None)
    print('date_from -> ', date_from)
    print('date_to -> ', date_to)
    # print("Home Data => ", data)
    response = requests.get(f'{settings.AMAN_API_URL}home/', params=data, verify=False)
    content = response.json()
    if not content['responseCode'] == 200:
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    count = 0
    t = []
    for p in content['responseData']['transactionsData']:
        count += 1
        t1 = {
            'amount': p['amount'],
            'transactionDate': p['transactionDate']
        }
        t.append(t1)
    queryset = content['responseData']['transactionsData']
    cards = {
        'count': {
            "points": ChartServices.generate_points(queryset, time_frame, date_from, date_to, "count")
        },
        'avg': {
            "points": ChartServices.generate_points(queryset, time_frame, date_from, date_to, "avg")
        },
        'sum': {
            "points": ChartServices.generate_points(queryset, time_frame, date_from, date_to, "sum")
        },
        'sum_card_info': {
            "points": ChartServices.generate_points(queryset, time_frame, date_from, date_to, "sum")
        },
        'category_card': content['responseData']['transactionsTypeInfo']
    }

    # print('cards', cards)

    count_current_overall = sum(p['value'] for p in cards['count']['points'])
    cards['count']['ratio'] = (count_current_overall - content['responseData']['comparedValues']['count']) / abs(content['responseData']['comparedValues']['count']) * 100 if content['responseData']['comparedValues']['count'] and content['responseData']['comparedValues']['count'] > 0 else 0
    cards['count']['total'] =  count_current_overall

    sum_current_overall = sum(p['value'] for p in cards['sum']['points'])
    cards['sum']['ratio'] = (sum_current_overall - content['responseData']['comparedValues']['total']) / abs(content['responseData']['comparedValues']['total']) * 100 if content['responseData']['comparedValues']['total'] and content['responseData']['comparedValues']['total'] > 0 else 0
    cards['sum']['total'] = sum_current_overall

    current_overall = sum_current_overall / count_current_overall if count_current_overall else 0
    cards['avg']['ratio'] = (current_overall - content['responseData']['comparedValues']['mean']) / abs(content['responseData']['comparedValues']['mean']) * 100 if content['responseData']['comparedValues']['mean'] and content['responseData']['comparedValues']['mean'] > 0 else 0
    cards['avg']['total'] = current_overall

    return Response(cards, status=200)
