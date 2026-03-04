import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.common.models import Farm, Parcel
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url='/users/signin/')
def index(request):
  farms = Farm.objects.all()
  context = {
    'segment': 'dashboard',
    'farms': farms
  }
  return render(request, "dashboard/index.html", context)


def create_farm(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    Farm.objects.get_or_create(
      name=name,
      user=request.user
    )
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))

def edit_farm(request, pk):
  farm = get_object_or_404(Farm, pk=pk)
  if request.method == 'POST':
    name = request.POST.get('name')
    farm.name = name
    farm.save()
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))

def delete_farm(request, pk):
  farm = get_object_or_404(Farm, pk=pk)
  farm.delete()
  return redirect(request.META.get('HTTP_REFERER'))

def farm_details(request, pk):
  farm = get_object_or_404(Farm, pk=pk)
  parcels_qs = Parcel.objects.filter(farm=farm)
  parcels = list(parcels_qs.values('id', 'polygon'))

  context = {
    'farm': farm,
    'parcels': parcels,
    'API_KEY': getattr(settings, 'GOOGLE_MAP_API_KEY')
  }
  return render(request, "dashboard/farm-details.html", context)

@login_required(login_url='/users/signin/')
def save_parcel(request, pk):
  farm = get_object_or_404(Farm, pk=pk, user=request.user)

  if request.method == "POST":
    polygon_data = request.POST.get("polygon")
    parcel_id = request.POST.get("parcel_id")

    if polygon_data:
      if parcel_id:
        parcel = get_object_or_404(Parcel, id=parcel_id, farm=farm)
        parcel.polygon = json.loads(polygon_data)
        parcel.save()
      else:
        Parcel.objects.create(
          farm=farm,
          polygon=json.loads(polygon_data)
        )

  return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def delete_parcel(request, farm_id, parcel_id):
  farm = get_object_or_404(Farm, pk=farm_id, user=request.user)
  parcel = get_object_or_404(Parcel, pk=parcel_id, farm=farm)

  parcel.delete()

  return redirect(request.META.get('HTTP_REFERER'))