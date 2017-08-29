from .models import Profile
from .serializers import ProfileSerializer

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


class CustomerProfileView(View):
    @staticmethod
    @login_required
    def get(request):
        customer = request.user

        if not Profile.exists_for_customer(customer):
            return redirect("/profile/create/")

        profile = Profile.objects.get(customer=customer)

        created = request.GET.get('created', False)

        return render(request, 'profile.html', {
            "view_profile": True,
            "profile": profile,
            "success_created": created
        })

    @staticmethod
    @login_required
    def post(request):
        customer = request.user
        redirect_to_cart = request.GET.get('redirect-to-cart', False)

        if not Profile.exists_for_customer(customer):
            return redirect("/profile/create/")

        profile = Profile.objects.get(customer=customer)
        serializer = ProfileSerializer(data=request.POST)

        if serializer.is_valid():
            profile.email = serializer.validated_data["email"]
            profile.phone = serializer.validated_data["phone"]
            profile.city = serializer.validated_data["city"]
            profile.address = serializer.validated_data["address"]
            profile.postal_code = serializer.validated_data["postal_code"]
            profile.save()

            if redirect_to_cart:
                return redirect("/cart/")
            else:
                return render(request, 'profile.html', {
                    "view_profile": True,
                    "profile": profile,
                    "success_modify": True
                })

        else:
            return render(request, 'profile.html', {
                "view_profile": True,
                "profile": profile,
                "errors": serializer.errors
            })


class CreateCustomerProfileView(View):
    @staticmethod
    @login_required
    def get(request):
        customer = request.user

        if Profile.exists_for_customer(customer):
            return redirect("/profile/")

        return render(request, 'profile.html', {
            "create_profile": True
        })

    @staticmethod
    @login_required
    def post(request):
        customer = request.user
        redirect_to_cart = request.GET.get('redirect-to-cart', False)

        if Profile.exists_for_customer(customer):
            return redirect("/profile/")

        serializer = ProfileSerializer(data=request.POST)

        if serializer.is_valid():
            Profile.objects.create(customer=customer,
                                   email=serializer.validated_data["email"],
                                   phone=serializer.validated_data["phone"],
                                   city=serializer.validated_data["city"],
                                   address=serializer.validated_data["address"],
                                   postal_code=serializer.validated_data["postal_code"])

            if redirect_to_cart:
                return redirect("/cart/")
            else:
                return redirect("/profile/?created=True")

        else:
            return render(request, 'profile.html', {
                "errors": serializer.errors
            })
