from django.conf.urls import url
from .views import *


waitlist_urls = [
    url(r'^waitlist/(?P<tier_id>(\d+))/$', WaitlistView.as_view()),
]
