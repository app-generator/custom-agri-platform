from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)

def starter(request):

  context = {}
  return render(request, "pages/starter.html", context)


# Layout
def stacked(request):
  context = {
    'segment': 'stacked',
    'parent': 'layouts'
  }
  return render(request, 'pages/layouts/stacked.html', context)

def sidebar(request):
  context = {
    'segment': 'sidebar',
    'parent': 'layouts'
  }
  return render(request, 'pages/layouts/sidebar.html', context)


# CRUD
def add_product(request):
  if request.method == 'POST':
    form_data = {}
    for attribute, value in request.POST.items():
      if attribute == 'csrfmiddlewaretoken':
        continue

      form_data[attribute] = value

    Product.objects.create(**form_data)

    return redirect(request.META.get('HTTP_REFERER'))

  return redirect(request.META.get('HTTP_REFERER'))

def edit_product(request, pk):
  product = Product.objects.get(pk=pk)

  if request.method == 'POST':
    for attribute, value in request.POST.items():
      if attribute == 'csrfmiddlewaretoken':
        continue

      setattr(product, attribute, value)
      product.save()

    return redirect(request.META.get('HTTP_REFERER'))

  return redirect(request.META.get('HTTP_REFERER'))

def delete_product(request, pk):
  product = Product.objects.get(pk=pk)
  product.delete()

  return redirect(request.META.get('HTTP_REFERER'))

def products(request):
  search_filter = {}
  if search := request.GET.get('search'):
    search_filter['name__icontains'] = search

  product_list = Product.objects.filter(**search_filter)

  page = request.GET.get('page', 1)
  paginator = Paginator(product_list, 10)

  try:
      products = paginator.page(page)
  except PageNotAnInteger:
      products = paginator.page(1)
  except EmptyPage:
      products = paginator.page(paginator.num_pages)

  context = {
    'segment': 'products',
    'parent': 'crud',
    'products': products,
    'technology': TechnologyChoice.choices,
    'discount': DiscountChoices.choices
  }
  return render(request, 'pages/CRUD/products.html', context)

def users(request):
  context = {
    'segment': 'users',
    'parent': 'crud'
  }
  return render(request, 'pages/CRUD/users.html', context)


# Pages
def pricing(request):
  return render(request, 'pages/pricing.html')

def maintenance(request):
  return render(request, 'pages/maintenance.html')

def error_404(request):
  return render(request, 'pages/404.html')

def error_500(request):
  return render(request, 'pages/500.html')

def settings_view(request):
  context = {
    'segment': 'settings',
  }
  return render(request, 'pages/settings.html', context)


# Playground
def stacked_playground(request):
  return render(request, 'pages/playground/stacked.html')


def sidebar_playground(request):
  context = {
    'segment': 'sidebar_playground',
    'parent': 'playground'
  }
  return render(request, 'pages/playground/sidebar.html', context)


# i18n
def i18n_view(request):
  context = {
    'segment': 'i18n'
  }
  return render(request, 'pages/i18n.html', context)
