from django.contrib import admin
from meter.models import Flow


class FlowAdmin(admin.ModelAdmin):
    search_fields = ['mpan', 'meter']
    list_display = ['mpan', 'meter', 'filename']
    

admin.site.register(Flow, FlowAdmin)
