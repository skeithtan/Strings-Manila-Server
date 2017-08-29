from django.conf.urls import url
from .views import *


waitlist_urls = [
    url(r'^waitlist/$', WaitlistListView.as_view()),
    url(r'^waitlist/(?P<tier_id>(\d+))/$', WaitlistDetailView.as_view()),
]
