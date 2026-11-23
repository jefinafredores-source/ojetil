from django.contrib import admin
from .models import OrganizationPosition, OrganizationUnit, StructureHistory


@admin.register(OrganizationUnit)
class OrganizationUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_type", "is_active")
    list_filter = ("unit_type", "is_active")
    search_fields = ("name",)


@admin.register(OrganizationPosition)
class OrganizationPositionAdmin(admin.ModelAdmin):
    list_display = ("title", "position_type", "person_name", "unit", "parent", "sort_order", "is_active")
    list_filter = ("position_type", "is_active")
    search_fields = ("title", "person_name")


@admin.register(StructureHistory)
class StructureHistoryAdmin(admin.ModelAdmin):
    list_display = ("title", "change_date")
