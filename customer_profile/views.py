from .models import Profile
from .serializers import ProfileSerializer

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

        if not profile_exists(customer):
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

            print(profile.address)

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

        if profile_exists(customer):
            return redirect("/profile/")

        return render(request, 'profile.html', {
            "create_profile": True
        })

    @staticmethod
    @login_required
    def post(request):
        customer = request.user

        if profile_exists(customer):
            return redirect("/profile/")

        serializer = ProfileSerializer(data=request.POST)

        if serializer.is_valid():
            Profile.objects.create(customer=customer,
                                   email=serializer.validated_data["email"],
                                   phone=serializer.validated_data["phone"],
                                   city=serializer.validated_data["city"],
                                   address=serializer.validated_data["address"],
                                   postal_code=serializer.validated_data["postal_code"])

            return redirect("/profile/?created=True")
        else:
            return render(request, 'profile.html', {
                "errors": serializer.errors
            })
