from django.contrib import admin
from .models import Municipality, PostoAdministrativo, Suco, Aldeia

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(PostoAdministrativo)
class PostoAdministrativoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'municipality')
    list_filter = ('municipality',)
    search_fields = ('name', 'municipality__name')

@admin.register(Suco)
class SucoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'posto_administrativo', 'get_municipality')
    list_filter = ('posto_administrativo__municipality', 'posto_administrativo')
    search_fields = ('name', 'posto_administrativo__name')

    @admin.display(ordering='posto_administrativo__municipality', description='Municipality')
    def get_municipality(self, obj):
        return obj.posto_administrativo.municipality

@admin.register(Aldeia)
class AldeiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'suco', 'get_posto', 'get_municipality')
    list_filter = ('suco__posto_administrativo__municipality', 'suco__posto_administrativo', 'suco')
    search_fields = ('name', 'suco__name')

    @admin.display(ordering='suco__posto_administrativo', description='Posto Administrativo')
    def get_posto(self, obj):
        return obj.suco.posto_administrativo

    @admin.display(ordering='suco__posto_administrativo__municipality', description='Municipality')
    def get_municipality(self, obj):
        return obj.suco.posto_administrativo.municipality