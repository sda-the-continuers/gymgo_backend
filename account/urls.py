from django.urls import path

from account.views import AthleteSMSLoginView, AthleteSMSSignupView, GymOwnerSMSLoginView, GymOwnerPasswordLoginView, \
    GymOwnerSMSSignupView, GymOwnerSetPasswordView, GymOwnerChangePasswordView, AccountLogout, AthleteProfileView, \
    GymOwnerProfileView, ProfilePictureView
from account.views.sms_entry_v2 import GymOwnerSMSEntryViewV2, AthleteSMSEntryViewV2


urlpatterns = [
    path('athlete/login/', AthleteSMSLoginView.as_view()),
    path('athlete/signup/', AthleteSMSSignupView.as_view()),
    path('gym-owner/sms-login/', GymOwnerSMSLoginView.as_view()),
    path('gym-owner/password-login/', GymOwnerPasswordLoginView.as_view()),
    path('gym-owner/signup/', GymOwnerSMSSignupView.as_view()),
    path('gym-owner/set-password/', GymOwnerSetPasswordView.as_view()),
    path('gym-owner/change-password/', GymOwnerChangePasswordView.as_view()),
    path('logout/', AccountLogout.as_view()),
    path('gym-owner/sms-entry/', GymOwnerSMSEntryViewV2.as_view()),
    path('athlete/sms-entry/', AthleteSMSEntryViewV2.as_view()),
    path('profile-picture/<int:pk>/', ProfilePictureView.as_view({'get': 'retrieve'})),
    path('profile-picture/', ProfilePictureView.as_view({'post': 'create'})),
    path('athlete/profile/', AthleteProfileView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    })),
    path('gym-owner/profile/', GymOwnerProfileView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    }))
]
