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

    path("parcel/<int:parcel_id>/crop-plan/create/", views.create_crop_plan, name="create_crop_plan"),
    path("crop-plan/<int:crop_plan_id>/action/add/", views.add_action, name="add_action"),
    path("parcel/<int:parcel_id>/plans/", views.parcel_plans, name="parcel_plans"),

    path("tabs/", views.tab_list, name="tab_list"),
    path("tab/create/", views.create_tab, name="create_tab"),
    path("tab/edit/<int:pk>/", views.edit_tab, name="edit_tab"),
    path("tab/delete/<int:pk>/", views.delete_tab, name="delete_tab"),
]
