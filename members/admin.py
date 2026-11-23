from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'member_id_code', 'position', 'district', 'membership_type', 'status', 'registration_date')
    list_filter = ('status', 'membership_type', 'position', 'district')
    search_fields = ('full_name', 'national_id', 'email', 'phone_number', 'member_id_code')