# financial_advisor/views.py

from django.shortcuts import render
from .advisor import get_financial_advice_data

def financial_advice_view(request):
    user = request.user
    advice_data = get_financial_advice_data(user)

    return render(request, 'financial_advisor.html', {'data': advice_data})
