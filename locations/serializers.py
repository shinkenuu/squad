from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import City, State


class CitySerializer(ModelSerializer):
    state = PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        model = City
        fields = ('name', 'state', )


class StateCitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name', )
