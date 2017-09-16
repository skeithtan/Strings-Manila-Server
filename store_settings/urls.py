from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^overview/$', SettingsOverview.as_view()),

    url(r'^maintenance-mode/enable/$', EnableMaintenanceMode.as_view()),
    url(r'^maintenance-mode/disable/$', DisableMaintenanceMode.as_view()),

    url(r'^bank-accounts/$', BankAccountList.as_view()),
    url(r'^bank-accounts/(?P<bank_account_id>(\d+))/$', BankAccountDetail.as_view())
]
