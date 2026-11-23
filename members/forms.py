from django import forms
from .models import Member
from locations.models import Municipality


class MemberRegistrationForm(forms.ModelForm):

    class Meta:
        model = Member

        fields = [
            'full_name', 'codigo', 'gender', 'date_of_birth',
            'place_of_birth', 'national_id', 'phone_number',
            'email', 'address', 'position', 'district',
            'membership_type', 'registration_date',
            'profile_photo', 'supporting_document'
        ]

        widgets = {
            'place_of_birth': forms.Select(attrs={
                'class': 'form-select',
            }),
            'district': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        municipalities = Municipality.objects.all()

        self.fields['place_of_birth'].queryset = municipalities
        self.fields['district'].queryset = municipalities