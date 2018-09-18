from django.urls import path

from .views import StateCitiesDetailView, StateCitiesListView


urlpatterns = [
    path('states/<str:state_name>/cities/', StateCitiesListView.as_view(), name='state-cities-list'),
    path('states/<str:state_name>/cities/<str:city_name>/', StateCitiesDetailView.as_view(), name='city-detail'),
]
