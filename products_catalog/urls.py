from django.conf.urls import url
from .views import *

urls = [
    url(r'^$', ProductCatalogView.as_view()),
    url(r'^cart/$', CartView.as_view()),
    url(r'^cart/review/$', ReviewOrderView.as_view()),
    url(r'^cart/finalize/$', FinalizeOrderView.as_view())
]