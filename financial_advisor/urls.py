from django.urls import path
from .views import financial_advice_view

urlpatterns = [
    path('', financial_advice_view, name='financial-advice'),
]