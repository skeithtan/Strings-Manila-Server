from django.conf.urls import url
from .views import *

customer_profile_urls = [
    url(r'^profile/$', CustomerProfileView.as_view()),
    url(r'^profile/edit/$', ModifyCustomerProfileView.as_view()),
    url(r'^profile/create/$', CreateCustomerProfileView.as_view())
]
