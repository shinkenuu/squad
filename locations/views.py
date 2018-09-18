from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import City, State
from .serializers import CitySerializer, StateCitySerializer


class StateCitiesListView(APIView):
    def get(self, request, *args, **kwargs):
        state_name = slugify(kwargs.get('state_name'))
        cities = get_list_or_404(City, state__name_slug=state_name)

        serializer = StateCitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        state_name = slugify(kwargs.get('state_name'))
        state = get_object_or_404(State, name_slug=state_name)

        data = request.data.copy()
        data['state'] = state.id

        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateCitiesDetailView(APIView):
    def get(self, request, *args, **kwargs):
        state_name = slugify(kwargs.get('state_name'))
        city_name = slugify(kwargs.get('city_name'))
        city = get_object_or_404(City, name_slug=city_name, state__name_slug=state_name)

        serializer = StateCitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
