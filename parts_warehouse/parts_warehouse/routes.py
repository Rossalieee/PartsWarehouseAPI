from django.urls import path, include
from rest_framework import routers

from base.views import CategoryViewSet, PartViewSet

router_api = routers.SimpleRouter()
router_api.register(r"categories", CategoryViewSet, basename="category")
router_api.register(r"parts", PartViewSet, basename="part")

api_urls = [
    path("", include(router_api.urls)),
]
