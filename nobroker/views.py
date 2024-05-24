from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from rest_framework import viewsets
from .models import Countries, States, Cities, Areas, FullHouse, PG, Flatmates
from .serializers import CountriesSerializer, StatesSerializer, CitiesSerializer, AreasSerializer, FullHouseSerializer, PGSerializer, FlatmatesSerializer

class CountriesViewSet(viewsets.ModelViewSet):
    queryset = Countries.objects.all()
    serializer_class = CountriesSerializer

class StatesViewSet(viewsets.ModelViewSet):
    queryset = States.objects.all()
    serializer_class = StatesSerializer

class CitiesViewSet(viewsets.ModelViewSet):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer

class AreasViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer

class FullHouseViewSet(viewsets.ModelViewSet):
    queryset = FullHouse.objects.all()
    serializer_class = FullHouseSerializer

class PGViewSet(viewsets.ModelViewSet):
    queryset = PG.objects.all()
    serializer_class = PGSerializer

class FlatmatesViewSet(viewsets.ModelViewSet):
    queryset = Flatmates.objects.all()
    serializer_class = FlatmatesSerializer


class CityAreaViewSet(viewsets.ViewSet):
    def list(self, request, city_id=None):
        try:
            areas = Areas.objects.filter(city_id=city_id)
            serializer = AreasSerializer(areas, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

class PgAreaViewSet(viewsets.ViewSet):
    def list(self, request, area_id=None):
        try:
            pgs = PG.objects.filter(area_id=area_id)
            serializer = PGSerializer(pgs, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)