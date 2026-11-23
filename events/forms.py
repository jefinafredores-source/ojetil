from django import forms
from .models import Event
from .models import Activity
from .models import ActivityCategory
from .models import EventInvitation

class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'title',
            'description',
            'event_date',
            'start_time',
            'end_time',
            'location',
            'event_type',
            'status',
            'max_participants',
            'participants',
            'image',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter event description'
            }),

            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event location'
            }),

            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),

            'participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


# ACTIVITY FORM
class ActivityForm(forms.ModelForm):

    class Meta:

        model = Activity

        fields = [
            'title',
            'description',
            'activity_date',
            'start_time',
            'end_time',
            'location',
            'category',
            'event',
            'status',
            'max_participants',
            'participants',
            'image',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter activity title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter activity description'
                }
            ),

            'activity_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'start_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter activity location'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'event': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'max_participants': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1
                }
            ),

            'participants': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

# ACTIVITY CATEGORY FORM

class ActivityCategoryForm(forms.ModelForm):
    class Meta:
        model = ActivityCategory
        fields = [
            "name",
            "description",
            "color",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Community Service",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Deskrisaun kona-ba kategoria...",
            }),
            "color": forms.TextInput(attrs={
                "class": "form-control form-control-color",
                "type": "color",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EventInvitationForm(forms.Form):

    TARGET_CHOICES = [
        ('event', 'Event'),
        ('activity', 'Activity'),
    ]

    target_type = forms.ChoiceField(
        choices=TARGET_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    event = forms.ModelChoiceField(
        queryset=Event.objects.all().order_by('-event_date'),
        required=False,
        empty_label='Select Event',
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all().order_by('-activity_date'),
        required=False,
        empty_label='Select Activity',
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    recipient_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Recipient name (optional)',
        })
    )

    recipient_organization = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Organization name (optional)',
        })
    )

    recipient_emails = forms.CharField(
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'placeholder': (
            'Hatama email sira iha ne\'e. '
            'Email ida kada linha ka separa ho virgula.'
        ),
    })
)

    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Invitation subject',
        })
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Write your invitation message...',
        })
    )

    def clean_recipient_emails(self):
        raw_emails = self.cleaned_data['recipient_emails']

        emails = raw_emails.replace(';', ',').replace('\n', ',').split(',')

        valid_emails = []

        for email in emails:
            email = email.strip()

            if not email:
                continue

            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError(
                    f'Email "{email}" la validu.'
                )

            if email.lower() not in [
                item.lower() for item in valid_emails
            ]:
                valid_emails.append(email)

        if not valid_emails:
            raise forms.ValidationError(
                'Hatama email destinatáriu ida pelo menus.'
            )

        return valid_emails

    def clean(self):
        cleaned_data = super().clean()

        target_type = cleaned_data.get('target_type')
        event = cleaned_data.get('event')
        activity = cleaned_data.get('activity')

        if target_type == 'event' and not event:
            self.add_error('event', 'Favor hili event ida.')

        if target_type == 'activity' and not activity:
            self.add_error('activity', 'Favor hili activity ida.')

        return cleaned_data       
