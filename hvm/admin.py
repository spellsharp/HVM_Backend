from django.contrib import admin

# Register your models here.

from .models import LeadVisitor, Accompanying, Receiver

class LeadVisitorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'unique_id', 'company_name', 'address', 'contact_number', 'visiting_date', 'visiting_time', 'image')
    list_filter = ('full_name', 'unique_id', 'company_name', 'address', 'contact_number', 'visiting_date', 'visiting_time', 'image')
    search_fields = ('full_name', 'unique_id', 'company_name', 'address', 'contact_number', 'visiting_date', 'visiting_time', 'image')


class AccompanyingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'unique_id', 'lead_visitor','contact_number')
    list_filter = ('full_name', 'unique_id', 'lead_visitor','contact_number')
    search_fields = ('full_name', 'unique_id', 'lead_visitor','contact_number')
    
class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'employee_id')
    list_filter = ('username', 'full_name', 'employee_id')
    search_fields = ('username', 'full_name', 'employee_id')


admin.site.register(LeadVisitor, LeadVisitorAdmin)
admin.site.register(Accompanying, AccompanyingAdmin)
admin.site.register(Receiver, ReceiverAdmin)