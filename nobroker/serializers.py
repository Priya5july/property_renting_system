from rest_framework import serializers
from .models import Countries, States, Cities, Areas, FullHouse, PG, Flatmates

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'

class FullHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullHouse
        fields = '__all__'

class PGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PG
        fields = '__all__'

class FlatmatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flatmates
        fields = '__all__'
