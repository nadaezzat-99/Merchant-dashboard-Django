from helpers.models import GeneralInfo
from helpers.serializers.general_info_serializers import GeneralInfoSerializer


class GeneralInfoServices:
    @staticmethod
    def get_privacy_and_policy(request):
        if GeneralInfo.objects.all().count() > 0:
            info = GeneralInfo.objects.all().last()
            lang = request.headers.get('Accept-Language')
            if lang == 'ar':
                return info.privacy_and_policy_ar, True
            return info.privacy_and_policy, True
        return "No Data To Retrieve", False


    @staticmethod
    def get_terms_and_conditions(request):
        if GeneralInfo.objects.all().count() > 0:
            info = GeneralInfo.objects.all().last()
            lang = request.headers.get('Accept-Language')
            if lang == 'ar':
                return info.terms_and_conditions_ar, True
            return info.terms_and_conditions, True
        return "No Data To Retrieve", False



    @staticmethod
    def get_social_media(request):
        if GeneralInfo.objects.all().count() > 0:
            info = GeneralInfo.objects.all().last()
            # print("#######2", info)
            info_serializer = GeneralInfoSerializer(instance=info, context={'fields': ['whatsapp_number', 'twitter_link', 'facebook_link']})
            # print("########1", info_serializer.data)
            return info_serializer.data, True
        return "No Data To Retrieve", False