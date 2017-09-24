from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *
from admin_auth.permissions import IsSuperuser


class MaterialsOverview(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):
        colors = Color.all_active()
        sizes = Size.all_active()

        colors = ColorSerializer(colors, many=True).data
        sizes = SizeSerializer(sizes, many=True).data

        # TODO: More data
        data = {
            "colors": colors,
            "sizes": sizes
        }

        return Response(data=data, status=200)


class ColorList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        serializer = ColorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(validated_data=serializer.data)
            return Response(status=200)
        else:
            return Response(data=serializer.errors, status=400)


class ColorDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def delete(request, color_id):
        color = get_object_or_404(Color, id=color_id)
        color.discontinue()
        return Response(status=200)


class SizeList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        serializer = SizeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(validated_data=serializer.data)
            return Response(status=200)
        else:
            return Response(data=serializer.errors, status=400)


class SizeDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def delete(request, size_id):
        size = get_object_or_404(Size, id=size_id)
        size.discontinue()
        return Response(status=200)
