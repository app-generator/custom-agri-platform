from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Farm
    path("farms/", views.farms, name="farms"),
    path("farm/create/", views.create_farm, name="create_farm"),
    path("farm/edit/<int:pk>/", views.edit_farm, name="edit_farm"),
    path("farm/delete/<int:pk>/", views.delete_farm, name="delete_farm"),
    path("farm/<int:pk>/", views.farm_details, name="farm_details"),
    path("add-farm-manager/<int:pk>/", views.add_farm_manager, name="add_farm_manager"),
    path('farm/<int:pk>/save-parcel/', views.save_parcel_polygon, name='save_parcel_polygon'),
    path('farm/<int:pk>/import-parcel/', views.import_parcel_polygon, name='import_parcel_polygon'),
    path('farm/<int:parcel_id>/parcel/<int:parcel_polygon_id>/delete/', views.delete_parcel_polygon, name='delete_parcel_polygon'),

    path('create/<int:farm_id>/parcel/', views.create_parcel, name='create_parcel'),
    path('edit/<int:pk>/parcel/', views.edit_parcel, name='edit_parcel'),
    path('delete/<int:pk>/parcel/', views.delete_parcel, name='delete_parcel'),
    path('detail/<int:pk>/parcel/', views.parcel_details, name='parcel_details'),

    path("parcel/<int:parcel_polygon_id>/crop-plan/create/", views.create_crop_plan, name="create_crop_plan"),
    path("crop-plan/<int:crop_plan_id>/action/add/", views.add_action, name="add_action"),
    path("parcel/<int:parcel_polygon_id>/plans/", views.parcel_plans, name="parcel_plans"),

    path("tabs/", views.tab_list, name="tab_list"),
    # path("tab/<int:pk>/", views.tab_detail, name="tab_detail"),
    path("tab/create/<int:sheet_id>/", views.create_tab, name="create_tab"),
    path("tab/edit/<int:pk>/", views.edit_tab, name="edit_tab"),
    path("tab/delete/<int:pk>/", views.delete_tab, name="delete_tab"),

    path("tab-row/edit/<int:pk>/", views.tab_row_edit, name="tab_row_edit"),
    path("tab-row/delete/<int:pk>/", views.tab_row_delete, name="tab_row_delete"),

    path("tab-row/upload/<int:pk>/", views.tab_row_upload, name="tab_row_upload"),

    #
    path("personnel/", views.personnel, name="personnel"),
    path("tasks/", views.tasks, name="tasks"),
    path("review-docs/", views.review_docs, name="review_docs"),
    path("pre-audit/", views.pre_audit, name="pre_audit"),
    path("search/", views.search, name="search"),
    path("certification/", views.certification, name="certification"),
    path("reports/", views.reports, name="reports"),

    path("role-request/", views.role_request, name="role_request"),
    path("onboarded/", views.onboarded_roles, name="onboarded_roles"),
    path("pending/", views.pending_invitations, name="pending_invitations"),
    path("invitation/<int:pk>/", views.remove_invitation, name="remove_invitation"),
    path("invite-personnel/", views.invite_personnel, name="invite_personnel"),
    path("invitations/accept/", views.accept_invitation, name="accept_invitation"),
    path("accept/request/<int:pk>/", views.accept_request, name="accept_request"),
    path("reject/request/<int:pk>/", views.reject_request, name="reject_request"),

    path("farms-to-request/", views.farms_to_request, name="farms_to_request"),
    path("send-request/<int:pk>/", views.send_request, name="send_request"),

    # Sheet
    path("tab/<int:pk>/", views.tab_details, name="tab_details"),
    path("sheet/edit/<int:pk>/", views.edit_sheet, name="edit_sheet"),
    path("sheet/delete/<int:pk>/", views.delete_sheet, name="delete_sheet"),

    path("field/edit/<int:pk>/", views.edit_field, name="edit_field"),
    path("field/delete/<int:pk>/", views.delete_field, name="delete_field"),
    path("add-new-field/<int:pk>/", views.add_new_field, name="add_new_field"),

    path("tab/<int:pk>/download-csv/", views.download_tab_csv, name="download_tab_csv"),
    path("asset/<int:row_id>/download/", views.download_asset, name="download_asset"),
    path("files/<int:pk>/", views.row_files, name="row_files"),
    path("upload-file/<int:pk>/", views.upload_file, name="upload_file"),
    path("delete-file/<int:pk>/", views.delete_file, name="delete_file"),

    path("add-data/<int:pk>/", views.add_data, name="add_data"),
]
