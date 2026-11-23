from .models import ActivityLog


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')

    if forwarded:
        return forwarded.split(',')[0].strip()

    return request.META.get('REMOTE_ADDR')


def log_activity(
    request,
    action,
    description,
    model_name='',
    object_id=''
):
    user = request.user if request.user.is_authenticated else None

    return ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
        model_name=model_name,
        object_id=str(object_id) if object_id else ''
    )