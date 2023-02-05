from django.urls import path

from sms.views.entry import SendSMSVerificationTokenView

urlpatterns = [
    path('send-token/', SendSMSVerificationTokenView.as_view()),
]