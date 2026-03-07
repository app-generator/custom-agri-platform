from django.contrib import admin

from apps.common.models import Sheet, Tab, TabFields
from django.apps import apps
from django.contrib import admin

# Register your models here.

# app_models = apps.get_app_config('common').get_models()
# for model in app_models:
#     try:    
 
#         admin.site.register(model)

#     except Exception:
#         pass


admin.site.register(Sheet)

class TabAdmin(admin.ModelAdmin):
    list_display = ('sheet', 'name', )

admin.site.register(Tab, TabAdmin)

class TabFieldsAdmin(admin.ModelAdmin):
    list_display = ('tab', 'name', )

admin.site.register(TabFields, TabFieldsAdmin)