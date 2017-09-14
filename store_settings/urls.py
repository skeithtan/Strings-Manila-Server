from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^overview/$', SettingsOverview.as_view()),
    url(r'^maintenance-mode/enable/$', EnableMaintenanceMode.as_view()),
    url(r'^maintenance-mode/disable/$', DisableMaintenanceMode.as_view()),
]
