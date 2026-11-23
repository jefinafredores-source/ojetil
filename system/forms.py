
from django import forms
from .models import GeneralSetting, OrganizationProfile
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm
from .models import AppearanceSetting, NotificationSetting


class GeneralSettingForm(forms.ModelForm):
    class Meta:
        model = GeneralSetting
        fields = [
            'site_name',
            'site_description',
            'contact_email',
            'contact_phone',
            'address',
            'logo',
        ]

        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'site_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            'organization_name',
            'abbreviation',
            'vision',
            'mission',
            'history',
            'email',
            'phone',
            'address',
        ]

        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'abbreviation': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'vision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'mission': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

        # Aumenta iha import iha leten forms.py




class UserCreateForm(UserCreationForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }


class UserEditForm(forms.ModelForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'is_active',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class RestoreDatabaseForm(forms.Form):

    backup_file = forms.FileField(
        label='Select SQLite Backup',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.sqlite3,.db'
        })
    )

    confirm_restore = forms.BooleanField(
        required=True,
        label='I understand that restoring will replace the current database.',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def clean_backup_file(self):
        file = self.cleaned_data['backup_file']

        if not file.name.lower().endswith(('.sqlite3', '.db')):
            raise forms.ValidationError(
                'Upload SQLite backup file (.sqlite3 or .db) deit.'
            )

        if file.size > 100 * 1024 * 1024:
            raise forms.ValidationError(
                'Backup file boot liu 100 MB.'
            )

        return file

class RoleForm(forms.ModelForm):

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related(
            'content_type'
        ).order_by(
            'content_type__app_label',
            'content_type__model',
            'codename'
        ),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': 12,
        }),
        label='Permissions'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Administrator'
            }),
        }

        
class AppearanceSettingForm(forms.ModelForm):
    class Meta:
        model = AppearanceSetting
        fields = [
            'theme',
            'sidebar_style',
            'primary_color',
            'compact_mode',
            'show_logo',
        ]
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'sidebar_style': forms.Select(attrs={'class': 'form-select'}),
            'primary_color': forms.TextInput(attrs={
                'class': 'form-control form-control-color',
                'type': 'color'
            }),
            'compact_mode': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'show_logo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class NotificationSettingForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = [
            'email_enabled',
            'in_app_enabled',
            'notify_new_member',
            'notify_member_status',
            'notify_new_event',
            'notify_backup',
            'notify_security',
        ]
        widgets = {
            field: forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
            for field in [
                'email_enabled',
                'in_app_enabled',
                'notify_new_member',
                'notify_member_status',
                'notify_new_event',
                'notify_backup',
                'notify_security',
            ]
        }
