import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.common.models import Farm, Parcel, CropPlan, CropType, Substance, ParcelAction, FarmMembership, Tag
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from apps.users.decorators import role_required
from apps.users.models import UserRole

from django.contrib.auth import get_user_model

User = get_user_model()


def landing(request):
  return render(request, 'pages/landing.html')

def dashboard(request):
  context = {
    'segment': 'dashboard',
    'title': 'Dashboard'
  }
  return render(request, "dashboard/index.html", context)

def farms(request):
  farms = Farm.objects.filter(
    farm_role__user=request.user,
    farm_role__active=True
  ).distinct()

  context = {
    'segment': 'farm',
    'farms': farms,
    'title': 'Farms'
  }

  return render(request, "pages/farms/index.html", context)

def create_farm(request):
  tags = Tag.objects.all()

  if request.method == 'POST':
    name = request.POST.get('name')
    address = request.POST.get('address')
    tags = request.POST.getlist('tags')
    lat = request.POST.get("latitude")
    lon = request.POST.get("longitude")

    farm = Farm.objects.create(
      name=name,
      address=address,
      lat=lat,
      lon=lon
    )
    farm.tags.set(tags)

    Role.objects.create(
      user=request.user,
      farm=farm,
      role=UserRole.ADMIN,
      active=True
    )
    return redirect(reverse('farms'))

  context = {
    'segment': 'farm',
    'title': 'Create new Farm',
    'tags': tags,
    'API_KEY': getattr(settings, 'GOOGLE_MAP_API_KEY'),
  }
  return render(request, "pages/farms/new.html", context)

def edit_farm(request, pk):
  farm = get_object_or_404(Farm, pk=pk)
  tags = Tag.objects.all()

  if request.method == 'POST':
    tags = request.POST.getlist('tags')

    farm.name = request.POST.get('name')
    farm.lat = request.POST.get("latitude")
    farm.lon = request.POST.get("longitude")
    farm.address = request.POST.get("address")

    farm.save()

    farm.tags.set(tags)

    return redirect(request.META.get('HTTP_REFERER'))
  
  context = {
    'farm': farm,
    'segment': 'farm',
    'title': 'Edit Farm',
    'tags': tags,
    'API_KEY': getattr(settings, 'GOOGLE_MAP_API_KEY'),
  }
  return render(request, "pages/farms/edit.html", context)

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
    'API_KEY': getattr(settings, 'GOOGLE_MAP_API_KEY'),
    'title': farm.name
  }
  return render(request, "dashboard/farm-details.html", context)


def add_farm_manager(request, pk):
  farm = get_object_or_404(Farm, pk=pk)
  if request.method == 'POST':
    user_id = request.POST.get('user')
    user = get_object_or_404(User, pk=user_id)

    role, created = Role.objects.update_or_create(
      farm=farm,
      role=UserRole.FARMER,
      defaults={
        'user': user,
        'active': True
      }
    )

    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))

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


def delete_parcel(request, farm_id, parcel_id):
  farm = get_object_or_404(Farm, pk=farm_id)
  parcel = get_object_or_404(Parcel, pk=parcel_id, farm=farm)

  parcel.delete()

  return redirect(request.META.get('HTTP_REFERER'))

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
from apps.common.models import Tab, Sheet, TabFields, TabCell, TabRow, Asset

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
    'segment': 'tab',
    'title': 'Tabs'
  }
  return render(request, 'pages/tabs/index.html', context)

def tab_detail(request, pk):
  tab = get_object_or_404(Tab, pk=pk)
  fields = list(TabFields.objects.filter(tab=tab).order_by("id"))
  rows_qs = TabRow.objects.filter(tab=tab).order_by("row_index")

  page_number = request.GET.get('page', 1) 
  paginator = Paginator(rows_qs, 10)
  try:
    rows = paginator.page(page_number)
  except PageNotAnInteger:
    rows = paginator.page(1)
  except EmptyPage:
    rows = paginator.page(paginator.num_pages)

  row_ids = [r.id for r in rows]
  cells = TabCell.objects.filter(row_id__in=row_ids)
  cell_map = {(c.row_id, c.field_id): c.value for c in cells}

  assets = Asset.objects.filter(row_id__in=row_ids)
  asset_map = {a.row_id: a for a in assets}

  table_data = []
  for row in rows:
    row_cells = []

    for field in fields:
      value = cell_map.get((row.id, field.id), "")
      row_cells.append(value)

    asset = asset_map.get(row.id)
    table_data.append((row, row_cells, asset))

  context = {
    "tab": tab,
    "fields": fields,
    "table_data": table_data,
    "rows": rows,
    "segment": "tab",
    "title": tab.name
  }

  return render(request, "pages/tabs/tab_detail.html", context)

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


def tab_row_edit(request, pk):
  row = get_object_or_404(TabRow, pk=pk)
  tab = row.tab

  fields = TabFields.objects.filter(tab=tab)

  cells = TabCell.objects.filter(row=row)
  cell_map = {c.field_id: c for c in cells}

  if request.method == "POST":
    for field in fields:
      value = request.POST.get(f"field_{field.id}")

      cell = cell_map.get(field.id)

      if cell:
        cell.value = value
        cell.save()
      else:
        TabCell.objects.create(
          row=row,
          field=field,
          value=value
        )

    return redirect(reverse('tab_detail', args=[tab.id]))

  context = {
    "row": row,
    "fields": fields,
    "cell_map": cell_map,
    "segment": "tab",
    "title": "Tab Rows"
  }

  return render(request, "pages/tabs/tab_row_edit.html", context)


def tab_row_delete(request, pk):
  row = get_object_or_404(TabRow, pk=pk)
  row.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def tab_row_upload(request, pk):
  row = get_object_or_404(TabRow, pk=pk)

  if request.method == "POST":
    file = request.FILES.get("asset")

    if file:
      Asset.objects.update_or_create(
        user=request.user,
        row=row,
        defaults={
          'file': file
        }
      )

      return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect(request.META.get('HTTP_REFERER'))


def personnel(request):
  context = {
    'segment': 'personnel',
    'title': 'Personnel'
  }
  return render(request, 'pages/farms/personnel.html', context)

def tasks(request):
  context = {
    'segment': 'tasks',
    'title': 'Tasks'
  }
  return render(request, 'pages/farms/tasks.html', context)

def review_docs(request):
  context = {
    'segment': 'review_docs',
    'title': 'Review Docs'
  }
  return render(request, 'pages/farms/review_docs.html', context)

def pre_audit(request):
  context = {
    'segment': 'pre_audit',
    'title': 'Pre Audit'
  }
  return render(request, 'pages/farms/pre_audit.html', context)

def search(request):
  context = {
    'segment': 'search',
    'title': 'Search'
  }
  return render(request, 'pages/farms/search.html', context)

def certification(request):
  context = {
    'segment': 'certification',
    'title': 'Certification'
  }
  return render(request, 'pages/farms/certification.html', context)

def reports(request):
  context = {
    'segment': 'reports',
    'title': 'Reports'
  }
  return render(request, 'pages/farms/reports.html', context)


# Request
from apps.common.models import Role

def role_request(request):
  pending_requests = Role.objects.filter(
    farm=request.user.active_farm,
    active=False
  )
  context = {
    'segment': 'request',
    'parent': 'personnel',
    'title': 'Role Request',
    'pending_requests': pending_requests
  }
  return render(request, 'pages/farms/role_request.html', context)


def onboarded_roles(request):
  onboarded_roles = Role.objects.filter(
    farm=request.user.active_farm,
    active=True
  )
  context = {
    'segment': 'onboarded',
    'parent': 'personnel',
    'title': 'Onboarded Roles',
    'onboarded_roles': onboarded_roles
  }
  return render(request, 'pages/farms/onboarded.html', context)

def accept_request(request, pk):
  role = get_object_or_404(Role, pk=pk)
  role.active = True
  role.save()
  return redirect(request.META.get('HTTP_REFERER'))


def reject_request(request, pk):
  role = get_object_or_404(Role, pk=pk)
  role.delete()
  return redirect(request.META.get('HTTP_REFERER'))