from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Farm
    path("farm/create/", views.create_farm, name="create_farm"),
    path("farm/edit/<int:pk>/", views.edit_farm, name="edit_farm"),
    path("farm/delete/<int:pk>/", views.delete_farm, name="delete_farm"),
    path("farm/<int:pk>/", views.farm_details, name="farm_details"),
    path('farm/<int:pk>/save-parcel/', views.save_parcel, name='save_parcel'),
    path('farm/<int:farm_id>/parcel/<int:parcel_id>/delete/', views.delete_parcel, name='delete_parcel'),
]
