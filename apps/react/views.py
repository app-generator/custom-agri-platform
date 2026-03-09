from django.shortcuts import render
from django.core import serializers

# Create your views here.

def index(request):
    # Page from the theme
    return render(request, "apps/react/index.html")

def charts(request):
    context = {
        'segment'  : 'react_charts',
        'parent'   : 'apps'
    }
    return render(request, 'apps/react/charts.html', context)