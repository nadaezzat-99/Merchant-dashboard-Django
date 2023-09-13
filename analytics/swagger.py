from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from analytics.views.transaction_views import savePOSTransactionDataView,setSettlementView
from analytics.views.pos_views import deletePosView



savePOSTransactionData = swagger_auto_schema(
    method='post',
    operation_description='Save pos transactions',
    request_body= openapi.Schema(type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_OBJECT,properties={
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='date of creation from aman side'),
            "merchant":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='terminal id'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),

                    }
                
            ),
            "pos":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'merchant_id': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'terminal_id': openapi.Schema(type=openapi.TYPE_STRING, description='terminal id'),
                        'serial_number': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'vendor_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'address': openapi.Schema(type=openapi.TYPE_STRING, description='address of the user'),
                        'terminal_type_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'acquire': openapi.Schema(type=openapi.TYPE_ARRAY,
                         items=openapi.Items(type=openapi.TYPE_OBJECT,properties={
                            "id":openapi.Schema(type=openapi.TYPE_STRING, description='acquire id'),
                            "name":openapi.Schema(type=openapi.TYPE_STRING, description='acquire name'),
                            })
                        ,description='array of acquire objects'),
                        "chain":openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='chain id'),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='chain name'),
                                }),

                    }
                
            ),
            "bank_details":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'bank_name': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
                        'bank_branch': openapi.Schema(type=openapi.TYPE_STRING, description='bank branch'),
                        'account_number': openapi.Schema(type=openapi.TYPE_STRING, description='account number'),
                    }
                
            ),
            "customer_details":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'issuer': openapi.Schema(type=openapi.TYPE_STRING, description='issuer'),
                        'pan': openapi.Schema(type=openapi.TYPE_STRING, description='pan'),
                        'card_holder_name': openapi.Schema(type=openapi.TYPE_STRING, description='card holder name'),
                    }
                
            ),
            
            "transaction":openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='transaction status whether to create to update',enum=['create','update']),
                        'amount': openapi.Schema(type=openapi.TYPE_STRING, description='amount'),
                        'mapping_type' : openapi.Schema(type=openapi.TYPE_STRING, description='mapping type'),
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description='type'),
                        'date': openapi.Schema(type=openapi.TYPE_STRING, description='date'),
                        'header1': openapi.Schema(type=openapi.TYPE_STRING, description='header1'),
                        'header2': openapi.Schema(type=openapi.TYPE_STRING, description='header2'),
                        'header3': openapi.Schema(type=openapi.TYPE_STRING, description='header3'),
                        'aman_batch_id': openapi.Schema(type=openapi.TYPE_STRING, description='aman batch id'),
                        'batch_id': openapi.Schema(type=openapi.TYPE_STRING, description='batch id'),
                        'stan': openapi.Schema(type=openapi.TYPE_STRING, description='stan'),
                        'is_settled': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='settled'),
                        'settlement_reference': openapi.Schema(type=openapi.TYPE_STRING, description='settlement reference'),
                        'settlement_date': openapi.Schema(type=openapi.TYPE_STRING, description='settlement date'),
                        'rrn': openapi.Schema(type=openapi.TYPE_STRING, description='rrn'),
                        'mdr': openapi.Schema(type=openapi.TYPE_STRING, description='mdr'),
                        'currency': openapi.Schema(type=openapi.TYPE_STRING, description='currency'),
                        'entry_mode': openapi.Schema(type=openapi.TYPE_STRING, description='entry_mode'),
                        'connection_on_off': openapi.Schema(type=openapi.TYPE_STRING, description='connection_on_off',enum=['online','offline']),
                        'emv_trx': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='emv trx'),
                        'dcc_trx': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='dcc trx'),
                        'is_installment': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='is installment'),
                        'is_void': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='is void'),
                        'response_code': openapi.Schema(type=openapi.TYPE_STRING, description='response code'),
                        'response_message': openapi.Schema(type=openapi.TYPE_STRING, description='response message'),
                        'auth_id': openapi.Schema(type=openapi.TYPE_STRING, description='auth id'),

                    }
                
            ),
        }),
   description='array of transaction objects'),
    responses={200: openapi.Response("Transactions saved successfully")}      
)(savePOSTransactionDataView)



deletePos = swagger_auto_schema(
    method='delete',
    operation_description='delete merchant pos',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='pos phone number'),
            'merchant_id': openapi.Schema(type=openapi.TYPE_STRING, description='merchant id'),
            'terminal_id': openapi.Schema(type=openapi.TYPE_STRING, description='termina id'),
            'deactivated': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='pos deactivation status'),
            'deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='pos deleted status'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='date of creation from aman side'),
        }),
    responses={200: openapi.Response("POS delete successfully")}
)(deletePosView)


setSettlement = swagger_auto_schema(
    method='post',
    operation_description='Set settlement',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'aman_batch_id': openapi.Schema(type=openapi.TYPE_STRING, description='batch number'),
            'batch_id': openapi.Schema(type=openapi.TYPE_STRING, description='batch number'),
            'transaction_ids': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='array of transaction ids'),
        }),
    responses={200: openapi.Response("POS's settled successfully")}
)(setSettlementView)