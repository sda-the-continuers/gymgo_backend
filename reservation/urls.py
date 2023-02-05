from django.urls import path

from reservation.views import AthleteReserveView

urlpatterns = [
    path(
        'reserve/', AthleteReserveView.as_view({'get': 'list'})
    ),
    path(
        'reserve/<int:pk>/', AthleteReserveView.as_view({'get': 'retrieve'})
    ),
]
