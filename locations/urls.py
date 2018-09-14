from django.urls import path

from .views import StateCitiesDetailView, StateCitiesListView


urlpatterns = [
    path('states/<slug:state_slug>/cities/', StateCitiesListView.as_view(), name='state-cities-list'),
    path('states/<slug:state_slug>/cities/<slug:city_slug>/', StateCitiesDetailView.as_view(), name='city-detail'),
]
