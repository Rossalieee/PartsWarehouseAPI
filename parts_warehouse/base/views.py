from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import Category, Part
from .serializers import CategorySerializer, PartSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get('q', '')

        parts = Part.objects.filter(
            Q(serial_number__icontains=q) |
            Q(name__icontains=q) |
            Q(category__name__icontains=q)
        )

        serializer = PartSerializer(parts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
