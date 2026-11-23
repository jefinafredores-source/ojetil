from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out
)
from django.dispatch import receiver

from .models import ActivityLog


def get_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')

    if forwarded:
        return forwarded.split(',')[0].strip()

    return request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):

    ActivityLog.objects.create(
        user=user,
        action='LOGIN',
        description=f'{user.username} tama iha sistema.',
        ip_address=get_ip(request)
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):

    if user:
        ActivityLog.objects.create(
            user=user,
            action='LOGOUT',
            description=f'{user.username} sai hosi sistema.',
            ip_address=get_ip(request)
        )