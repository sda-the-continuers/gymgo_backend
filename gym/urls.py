from django.urls import path

from gym.views import (
    FavoriteSportsView,
    AthleteGymComplexView,
    GymUsageView,
    ScheduledSessionView,
    ClubContactsView,
    SendSMSToClubContactsView,
    SendSMSForDiscountToClubContactsView, GymOwnerGymComplex,
)

urlpatterns = [
    path(
        'favorite-sports/', FavoriteSportsView.as_view({
            'get': 'list',
            'patch': 'partial_update',
        })
    ),
    path(
        'gym-complex/<str:code>/', AthleteGymComplexView.as_view({
            'get': 'retrieve',
        })
    ),
    path(
        'v2/gym-complex/<int:pk>/', AthleteGymComplexView.as_view({
            'get': 'retrieve',
        }, lookup_field='pk')
    ),
    path(
        'gym-complex/', GymOwnerGymComplex.as_view({
            'post': 'create',
        })
    ),
    path(
        'gym-usage/<int:pk>/', GymUsageView.as_view({
            'get': 'retrieve',
        })
    ),
    path('scheduled-session/', ScheduledSessionView.as_view()),
    path('club-contacts/', ClubContactsView.as_view({'get': 'list'})),
    path('club-contacts/<int:pk>/', ClubContactsView.as_view({'get': 'retrieve'})),
    path('club-sms/', SendSMSToClubContactsView.as_view()),
    path('club-discount-sms/', SendSMSForDiscountToClubContactsView.as_view()),
]
