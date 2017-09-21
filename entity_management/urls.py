from django.conf.urls import url
from .views import *

urls = [
    url(r'^collections/$', CollectionList.as_view()),
    url(r'^collections/(?P<collection_id>(\d+))/$', CollectionDetail.as_view()),
    url(r'^collections/(?P<collection_id>(\d+))/products/$', ProductList.as_view()),
    url(r'^products/(?P<product_id>(\d+))/$', ProductDetail.as_view()),
    url(r'^product-tiers/(?P<tier_id>(\d+))/restock/$', RestockTierView.as_view()),
]
