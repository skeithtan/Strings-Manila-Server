from django.conf.urls import url
from .views import *

urls = [
    url(r'^profile/$', CustomerProfileView.as_view()),
    url(r'^profile/create/$', CreateCustomerProfileView.as_view())
]
