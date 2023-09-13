from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helpers.services.general_info_services import GeneralInfoServices


# Create your views here.


@api_view(['GET', ])
def privacy_and_policy(request):
    data, success = GeneralInfoServices.get_privacy_and_policy(request)
    if not success:
        return Response({'error': data}, status=200)
    return Response(data, status=200)

@api_view(['GET', ])
def terms_and_conditions(request):
    data, success = GeneralInfoServices.get_terms_and_conditions(request)
    if not success:
        return Response({'error': data}, status=200)
    return Response(data, status=200)


@api_view(['GET', ])
def social_media(request):
    data, success = GeneralInfoServices.get_social_media(request)
    if not success:
        return Response({'error': data}, status=200)
    return Response(data, status=200)
