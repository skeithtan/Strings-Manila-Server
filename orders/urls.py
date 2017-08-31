from django.conf.urls import url

from .admin_views import *
from .customer_views import OrdersView
from .shared_views import CancelOrderView

order_api_urls = [
    url(r'^api/orders/$', OrderList.as_view()),
    url(r'^api/orders/(?P<order_id>(\d+))/$', OrderDetail.as_view()),
    url(r'^api/orders/(?P<order_id>(\d+))/cancel/$', CancelOrderView.as_view())
]

order_pages_urls = [
    url(r'^orders/$', OrdersView.as_view())
]

