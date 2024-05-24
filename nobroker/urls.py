from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'countries', CountriesViewSet)
router.register(r'states', StatesViewSet)
router.register(r'cities', CitiesViewSet)
router.register(r'areas', AreasViewSet)
router.register(r'fullhouses', FullHouseViewSet)
router.register(r'pgs', PGViewSet)
router.register(r'flatmates', FlatmatesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('city/<int:city_id>/areas/', CityAreaViewSet.as_view({'get': 'list'}), name='area-list-by-city'),  
    path('pg/<int:area_id>/', PgAreaViewSet.as_view({'get': 'list'}), name='pg-list-by-area'),  
]

