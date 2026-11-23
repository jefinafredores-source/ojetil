from django import forms
from .models import OrganizationPosition, OrganizationUnit, StructureHistory


class OrganizationUnitForm(forms.ModelForm):
    class Meta:
        model = OrganizationUnit
        fields = [
            "name",
            "unit_type",
            "description",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "unit_type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class OrganizationPositionForm(forms.ModelForm):
    class Meta:
        model = OrganizationPosition
        fields = [
            "title",
            "position_type",
            "person_name",
            "parent",
            "unit",
            "description",
            "sort_order",
            "color",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "position_type": forms.Select(attrs={"class": "form-select"}),
            "person_name": forms.TextInput(attrs={"class": "form-control"}),
            "parent": forms.Select(attrs={"class": "form-select"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(
                attrs={"class": "form-control", "type": "color"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class StructureHistoryForm(forms.ModelForm):
    class Meta:
        model = StructureHistory
        fields = ["title", "description", "change_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "change_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }