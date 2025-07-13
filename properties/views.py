from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import Property
from .serializers import PropertySerializer
from .utils import get_all_properties

@method_decorator(cache_page(60 * 15), name='dispatch')
class PropertyListView(viewsets.ViewSet):
    def list(self, request):
        queryset = get_all_properties()
        serializer = PropertySerializer(queryset, many=True)
        return JsonResponse({
            "data": serializer.data
        })
