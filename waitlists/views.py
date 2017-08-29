from .models import Waitlist
from entity_management.models import ProductTier

from rest_framework.views import APIView
from rest_framework.response import Response

from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


class WaitlistListView(View):
    @staticmethod
    @login_required
    def get(request):
        rows = []

        customer = request.user
        waitlist = Waitlist.objects.all().filter(customer=customer)
        for item in waitlist:
            tier = None if item.tier.product_description.is_singular else item.tier.name

            rows.append({
                "image": item.tier.product_description.image,
                "tier_id": item.tier.id,
                "tier_name": tier,
                "waitlist_date": item.date,
                "product_name": item.tier.product_description.name,
            })

        return render(request, 'waitlists.html', {
            "rows": rows
        })


class WaitlistDetailView(APIView):
    @staticmethod
    @login_required
    def post(request, tier_id):
        tier = get_object_or_404(ProductTier, id=tier_id)
        customer = request.user

        not_waitlisted = Waitlist.objects.all().filter(tier=tier, customer=customer).count() == 0

        if not_waitlisted:
            Waitlist.objects.create(tier=tier, customer=customer)

        return Response(status=200)

    @staticmethod
    @login_required
    def delete(request, tier_id):
        tier = get_object_or_404(ProductTier, id=tier_id)
        customer = request.user

        waitlist = get_object_or_404(Waitlist, tier=tier, customer=customer)
        waitlist.delete()

        return Response(status=200)
