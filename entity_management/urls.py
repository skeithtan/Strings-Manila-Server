from django.conf.urls import url
from .views import *

urls = [
    url(r'^stalls/$', StallList.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/$', StallDetail.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/$', ProductList.as_view()),
    url(r'^products/(?P<product_id>(\d+))/$', ProductDetail.as_view()),
    url(r'^product-tiers/(?P<tier_id>(\d+))/restock/$', RestockTierView.as_view()),
]
