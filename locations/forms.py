from django import forms
from .models import (
    Municipality,
    PostoAdministrativo,
    Suco,
    Aldeia
)


class MunicipalityForm(forms.ModelForm):
    class Meta:
        model = Municipality
        fields = ['name']


class PostoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = PostoAdministrativo
        fields = ['municipality', 'name']


class SucoForm(forms.ModelForm):
    class Meta:
        model = Suco
        fields = ['name', 'posto_administrativo']


class AldeiaForm(forms.ModelForm):
    class Meta:
        model = Aldeia
        fields = ['suco', 'name']