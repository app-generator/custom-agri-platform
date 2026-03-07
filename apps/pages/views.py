import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.common.models import Farm, Parcel, CropPlan, CropType, Substance, ParcelAction
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

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

  crop_plans = CropPlan.objects.filter(parcel__farm=farm).select_related('parcel', 'crop_type')
  crop_types = CropType.objects.all()
  substances = Substance.objects.all()

  context = {
    'farm': farm,
    'parcels': parcels,
    'crop_plans': crop_plans,
    'crop_types': crop_types,
    'substances': substances,
    'API_KEY': getattr(settings, 'GOOGLE_MAP_API_KEY')
  }
  return render(request, "dashboard/farm-details.html", context)

@login_required(login_url='/users/signin/')
def save_parcel(request, pk):
  farm = get_object_or_404(Farm, pk=pk)

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
  farm = get_object_or_404(Farm, pk=farm_id)
  parcel = get_object_or_404(Parcel, pk=parcel_id, farm=farm)

  parcel.delete()

  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def create_crop_plan(request, parcel_id):
  parcel = get_object_or_404(Parcel, id=parcel_id)

  if request.method == "POST":
    crop_type = request.POST.get("crop_type")
    year = request.POST.get("year")

    CropPlan.objects.create(
      parcel=parcel,
      crop_type_id=crop_type,
      year=year
    )

  return redirect(request.META.get("HTTP_REFERER"))

@login_required
def add_action(request, crop_plan_id):
  crop_plan = get_object_or_404(CropPlan, id=crop_plan_id)

  if request.method == "POST":
    action_type = request.POST.get("action_type")
    substance = request.POST.get("substance")
    date = request.POST.get("date")

    ParcelAction.objects.create(
      crop_plan=crop_plan,
      action_type=action_type,
      substance_id=substance if substance else None,
      date=date
    )

  return redirect(request.META.get("HTTP_REFERER"))


def parcel_plans(request, parcel_id):
  plans = CropPlan.objects.filter(parcel_id=parcel_id).select_related("crop_type")
  data = []
  for p in plans:
    actions = []

    for a in p.actions.all():
      actions.append({
        "type": a.action_type,
        "date": str(a.date),
        "substance": a.substance.name if a.substance else None
      })

    data.append({
      "id": p.id,
      "crop": p.crop_type.name,
      "year": p.year,
      "actions": actions
    })

  return JsonResponse(data, safe=False)


#
from apps.common.models import Tab, Sheet

def tab_list(request):
  tabs = Tab.objects.all()
  sheets = Sheet.objects.all()

  page_number = request.GET.get('page', 1) 
  paginator = Paginator(tabs, 9)
  try:
    tabs = paginator.page(page_number)
  except PageNotAnInteger:
    tabs = paginator.page(1)
  except EmptyPage:
    tabs = paginator.page(paginator.num_pages)

  context = {
    'tabs': tabs,
    'sheets': sheets,
    'segment': 'tab'
  }
  return render(request, 'pages/tabs/index.html', context)


def create_tab(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    sheet_id = request.POST.get('sheet')
    Tab.objects.get_or_create(
      name=name,
      sheet=get_object_or_404(Sheet, pk=sheet_id)
    )
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))

def edit_tab(request, pk):
  tab = get_object_or_404(Tab, pk=pk)
  if request.method == 'POST':
    name = request.POST.get('name')
    sheet_id = request.POST.get('sheet')
    tab.name = name
    tab.sheet =  get_object_or_404(Sheet, pk=sheet_id)
    tab.save()
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))

def delete_tab(request, pk):
  tab = get_object_or_404(Tab, pk=pk)
  tab.delete()
  return redirect(request.META.get('HTTP_REFERER'))