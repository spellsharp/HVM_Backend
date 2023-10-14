from django.contrib import admin

# Register your models here.

from .models import LeadVisitor, Accompanying

class LeadVisitorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'address', 'contact_number', 'visiting_time', 'image')
    list_filter = ('full_name', 'company_name', 'address', 'contact_number', 'visiting_time', 'image')
    search_fields = ('full_name', 'company_name', 'address', 'contact_number', 'visiting_time', 'image')


class AccompanyingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'lead_visitor','contact_number')
    list_filter = ('full_name', 'lead_visitor','contact_number')
    search_fields = ('full_name', 'lead_visitor','contact_number')


admin.site.register(LeadVisitor, LeadVisitorAdmin)
admin.site.register(Accompanying, AccompanyingAdmin)