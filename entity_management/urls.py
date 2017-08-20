from django.conf.urls import url
from .views import *

entity_management_urls = [
    url(r'^stalls/$', StallList.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/$', StallDetail.as_view()),
]
