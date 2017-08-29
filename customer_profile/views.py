from .models import Profile

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def profile_exists(customer):
    return Profile.objects.filter(customer=customer).count() >= 1


class CustomerProfileView(View):
    @staticmethod
    @login_required
    def get(request):
        customer = request.user

        if not profile_exists(customer):
            return redirect("/profile/create/")

            # TODO


class ModifyCustomerProfileView(View):
    @staticmethod
    @login_required
    def get(request):
        # TODO
        pass


class CreateCustomerProfileView(View):
    @staticmethod
    @login_required
    def get(request):
        customer = request.user

        if profile_exists(customer):
            return redirect("/profile/")

        return render(request, 'profile.html')
