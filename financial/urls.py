from django.urls import path

from financial.views.transactions import TransactionsView

urlpatterns = [
    path('transactions/', TransactionsView.as_view({'get': 'list'})),
    path('transactions/<int:pk>/', TransactionsView.as_view({'get': 'retrieve'})),
]
