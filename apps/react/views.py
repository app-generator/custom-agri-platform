from django.shortcuts import render
from apps.common.models import Product
from django.core import serializers

# Create your views here.

def index(request):
    # Page from the theme
    return render(request, "apps/react/index.html")

def charts(request):
    products = serializers.serialize('json', Product.objects.all())
    context = {
        'segment'  : 'react_charts',
        'parent'   : 'apps',
        'products': products
    }
    return render(request, 'apps/react/charts.html', context)