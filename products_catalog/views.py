from django.views import View
from django.shortcuts import render


class ProductCatalogView(View):
    @staticmethod
    def get(request):
        return render(request, 'products_catalog.html')
