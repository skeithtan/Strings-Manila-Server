from django.conf.urls import url
from .views import *

products_catalog_urls = [
    url(r'^$', ProductCatalogView.as_view()),
    url(r'^cart/$', CartView.as_view())
]