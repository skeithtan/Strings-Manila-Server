from .models import Waitlist
from entity_management.models import ProductTier

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


class WaitlistView(APIView):
    @staticmethod
    def post(request, tier_id):
        if not request.user.is_authenticated:
            return Response(data={
                "error": "User must be authenticated"
            }, status=400)

        tier = get_object_or_404(ProductTier, id=tier_id)
        user = request.user

        not_waitlisted = Waitlist.objects.all().filter(tier=tier, customer=user).count() == 0

        if not_waitlisted:
            Waitlist.objects.create(tier=tier, customer=user)

        return Response(status=200)
