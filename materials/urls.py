from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^overview/$', MaterialsOverview.as_view()),
    url(r'^colors/$', ColorList.as_view()),
    url(r'^colors/(?P<color_id>(\d+))/$', ColorDetail.as_view()),
]
