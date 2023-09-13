from django.urls import path,include

from analytics.views.export_views import export
from analytics.views.home_views import home
from analytics.views.report_views import report
from analytics.views.statistics_views import pos_statistics
from analytics.swagger import *
from helpers.views import privacy_and_policy, terms_and_conditions, social_media

urlpatterns = [
    path('POSstatistics', pos_statistics, name='POSstatistics'),
    path('export', export, name='export'),
    path('report', report, name='report'),
    path('home', home, name='home'),
    path('save_transaction', savePOSTransactionDataView, name='savePOSTransactionData'),
    path('privacy_and_policy', privacy_and_policy, name='PrivacyAndPolicy'),
    path('terms_and_conditions', terms_and_conditions, name='TermsAndConditions'),
    path('social_media', social_media, name='SocialMedia'),
    path('delete_pos', deletePosView, name='deletePosView'),
    path('set_settlement', setSettlementView, name='setSettlementView'),


]
urlpatterns = [
    path('/analytics/', include(urlpatterns)),
    
]