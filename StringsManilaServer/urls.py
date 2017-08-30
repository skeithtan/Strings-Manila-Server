"""StringsManilaServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from graphene_django.views import GraphQLView

from django.contrib import admin
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from orders.urls import admin_order_urls, customer_order_urls
from entity_management.urls import entity_management_urls
from products_catalog.urls import products_catalog_urls
from customer_profile.urls import customer_profile_urls
from waitlists.urls import waitlist_urls
from admin_auth.views import SignInView

urlpatterns = [
    url(r'^database/', admin.site.urls),
    url(r'^admin/sign-in/', SignInView.as_view()),
    url(r'^graphiql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^accounts/', include('allauth.urls')),
]

urlpatterns += entity_management_urls
urlpatterns += products_catalog_urls
urlpatterns += customer_profile_urls
urlpatterns += waitlist_urls
urlpatterns += admin_order_urls
urlpatterns += customer_order_urls

