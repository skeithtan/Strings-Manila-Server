from django.conf.urls import url

from .admin_views import *

admin_order_urls = [
    url(r'^api/orders/$', OrderList.as_view()),
    url(r'^api/orders/(?P<order_id>(\d+))/$', OrderDetail.as_view())
]

customer_order_urls = [
    # url(r'^orders/$')
]