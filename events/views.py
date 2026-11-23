
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

import calendar as pycalendar
from datetime import date

from .models import (
    Event,
    Activity,
    ActivityCategory,
    EventInvitation,
)

from .forms import (
    EventForm,
    ActivityForm,
    ActivityCategoryForm,
    EventInvitationForm,
)


# =====================================================
# EVENTS VIEWS
# =====================================================

def event_list(request):

    events = Event.objects.all().order_by(
        '-event_date',
        '-start_time'
    )

    context = {
        'events': events,
        'total_events': Event.objects.count(),

        'upcoming_events': Event.objects.filter(
            status='Upcoming'
        ).count(),

        'ongoing_events': Event.objects.filter(
            status='Ongoing'
        ).count(),

        'completed_events': Event.objects.filter(
            status='Completed'
        ).count(),

        'cancelled_events': Event.objects.filter(
            status='Cancelled'
        ).count(),
    }

    return render(
        request,
        'events/event.html',
        context
    )


def event_create(request):

    if request.method == 'POST':

        form = EventForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            event = form.save()

            messages.success(
                request,
                f'Event "{event.title}" created successfully.'
            )

            return redirect('events:event_list')

    else:
        form = EventForm()

    return render(
        request,
        'events/event_form.html',
        {
            'form': form,
            'page_title': 'Create Event',
            'button_text': 'Create Event'
        }
    )


def event_detail(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    return render(
        request,
        'events/event_detail.html',
        {
            'event': event
        }
    )


def event_update(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    if request.method == 'POST':

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():

            event = form.save()

            messages.success(
                request,
                f'Event "{event.title}" updated successfully.'
            )

            return redirect('events:event_list')

    else:

        form = EventForm(
            instance=event
        )

    return render(
        request,
        'events/event_form.html',
        {
            'form': form,
            'event': event,
            'page_title': 'Edit Event',
            'button_text': 'Update Event'
        }
    )


def event_delete(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    if request.method == 'POST':

        title = event.title

        event.delete()

        messages.success(
            request,
            f'Event "{title}" deleted successfully.'
        )

        return redirect('events:event_list')

    return render(
        request,
        'events/event_confirm_delete.html',
        {
            'event': event
        }
    )


# =====================================================
# ACTIVITIES LIST
# =====================================================

def activity_list(request):

    activities = Activity.objects.select_related(
        'category',
        'event'
    ).all().order_by(
        '-activity_date',
        '-start_time'
    )

    # SEARCH

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        activities = activities.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    # CATEGORY FILTER

    category = request.GET.get(
        'category',
        ''
    )

    if category:

        activities = activities.filter(
            category_id=category
        )

    # STATUS FILTER

    status = request.GET.get(
        'status',
        ''
    )

    if status:

        activities = activities.filter(
            status=status
        )

    # DATE FILTER

    selected_date = request.GET.get(
        'date',
        ''
    )

    if selected_date:

        activities = activities.filter(
            activity_date=selected_date
        )

    # STATISTICS

    total_activities = Activity.objects.count()

    ongoing_activities = Activity.objects.filter(
        status='Ongoing'
    ).count()

    completed_activities = Activity.objects.filter(
        status='Completed'
    ).count()

    upcoming_activities = Activity.objects.filter(
        status='Upcoming'
    ).count()

    # PAGINATION

    paginator = Paginator(
        activities,
        15
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    )

    # UPCOMING ACTIVITIES

    upcoming_list = Activity.objects.filter(
        status='Upcoming'
    ).order_by(
        'activity_date',
        'start_time'
    )[:5]

    context = {
        'activities': page_obj,
        'page_obj': page_obj,

        'total_activities': total_activities,
        'ongoing_activities': ongoing_activities,
        'completed_activities': completed_activities,
        'upcoming_activities': upcoming_activities,

        'upcoming_list': upcoming_list,

        'search': search,
        'selected_category': category,
        'selected_status': status,
        'selected_date': selected_date,

        # Permission ba template
        'can_edit_activity': request.user.has_perm(
            'events.change_activity'
        ),

        'can_delete_activity': request.user.has_perm(
            'events.delete_activity'
        ),
    }

    return render(
        request,
        'events/activity.html',
        context
    )


# =====================================================
# ACTIVITY CREATE
# =====================================================

@login_required
@permission_required(
    'events.add_activity',
    raise_exception=True
)
def activity_create(request):

    if request.method == 'POST':

        form = ActivityForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            activity = form.save()

            messages.success(
                request,
                f'Activity "{activity.title}" created successfully.'
            )

            return redirect(
                'events:activity_list'
            )

    else:

        form = ActivityForm()

    return render(
        request,
        'events/activity_form.html',
        {
            'form': form,
            'page_title': 'Create Activity',
            'button_text': 'Create Activity'
        }
    )


# =====================================================
# ACTIVITY DETAIL
# =====================================================

def activity_detail(request, pk):

    activity = get_object_or_404(
        Activity,
        pk=pk
    )

    return render(
        request,
        'events/activity_detail.html',
        {
            'activity': activity
        }
    )


# =====================================================
# ACTIVITY UPDATE
# MEMBER BELE EDIT SE HUSI IHA PERMISSION
# =====================================================

@login_required
@permission_required(
    'events.change_activity',
    raise_exception=True
)
def activity_update(request, pk):

    activity = get_object_or_404(
        Activity,
        pk=pk
    )

    if request.method == 'POST':

        form = ActivityForm(
            request.POST,
            request.FILES,
            instance=activity
        )

        if form.is_valid():

            activity = form.save()

            messages.success(
                request,
                f'Activity "{activity.title}" updated successfully.'
            )

            return redirect(
                'events:activity_list'
            )

    else:

        form = ActivityForm(
            instance=activity
        )

    return render(
        request,
        'events/activity_form.html',
        {
            'form': form,
            'activity': activity,
            'page_title': 'Edit Activity',
            'button_text': 'Update Activity'
        }
    )


# =====================================================
# ACTIVITY DELETE
# MEMBER LA BELE DELETE
# =====================================================

@login_required
@permission_required(
    'events.delete_activity',
    raise_exception=True
)
def activity_delete(request, pk):

    activity = get_object_or_404(
        Activity,
        pk=pk
    )

    # Delete deit bainhira uza POST

    if request.method == 'POST':

        title = activity.title

        activity.delete()

        messages.success(
            request,
            f'Activity "{title}" deleted successfully.'
        )

        return redirect(
            'events:activity_list'
        )

    return render(
        request,
        'events/activity_confirm_delete.html',
        {
            'activity': activity
        }
    )


# =====================================================
# ACTIVITY CATEGORY VIEWS
# =====================================================

def activity_category_list(request):

    categories = ActivityCategory.objects.annotate(
        activity_count=Count("activities")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    )

    if search:

        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if status == "active":

        categories = categories.filter(
            is_active=True
        )

    elif status == "inactive":

        categories = categories.filter(
            is_active=False
        )

    context = {
        "categories": categories,
        "search": search,
        "selected_status": status,

        "total_categories": ActivityCategory.objects.count(),

        "active_categories": ActivityCategory.objects.filter(
            is_active=True
        ).count(),

        "inactive_categories": ActivityCategory.objects.filter(
            is_active=False
        ).count(),

        "total_activities": sum(
            category.activity_count
            for category in categories
        ),
    }

    return render(
        request,
        "events/activity_category.html",
        context
    )


def activity_category_create(request):

    if request.method == "POST":

        form = ActivityCategoryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Activity category created successfully."
            )

            return redirect(
                "events:activity_category_list"
            )

    else:

        form = ActivityCategoryForm()

    return render(
        request,
        "events/activity_category_form.html",
        {
            "form": form,
            "page_title": "Add Category"
        }
    )


def activity_category_update(request, pk):

    category = get_object_or_404(
        ActivityCategory,
        pk=pk
    )

    if request.method == "POST":

        form = ActivityCategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Activity category updated successfully."
            )

            return redirect(
                "events:activity_category_list"
            )

    else:

        form = ActivityCategoryForm(
            instance=category
        )

    return render(
        request,
        "events/activity_category_form.html",
        {
            "form": form,
            "category": category,
            "page_title": "Edit Category",
        }
    )


def activity_category_delete(request, pk):

    category = get_object_or_404(
        ActivityCategory,
        pk=pk
    )

    if request.method == "POST":

        if category.activities.exists():

            messages.error(
                request,
                "Category has activities. Reassign them before deleting."
            )

        else:

            category.delete()

            messages.success(
                request,
                "Activity category deleted successfully."
            )

    return redirect(
        "events:activity_category_list"
    )


# =====================================================
# CALENDAR VIEW
# =====================================================

def calendar_view(request):

    today = timezone.localdate()

    month_param = request.GET.get(
        "month",
        ""
    )

    try:

        if month_param:

            selected_date = date.fromisoformat(
                month_param + "-01"
            )

        else:

            selected_date = today.replace(
                day=1
            )

    except (ValueError, TypeError):

        selected_date = today.replace(
            day=1
        )

    year = selected_date.year
    month = selected_date.month

    month_names = [
        "",
        "Janeiro", "Fevereiro", "Março",
        "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro",
        "Outubro", "Novembro", "Dezembro",
    ]

    month_label = f"{month_names[month]} {year}"

    # EVENTS THIS MONTH

    month_events = Event.objects.filter(
        event_date__year=year,
        event_date__month=month,
    ).order_by(
        "event_date",
        "start_time"
    )

    # UPCOMING EVENTS

    upcoming_events = Event.objects.filter(
        event_date__gte=today,
    ).order_by(
        "event_date",
        "start_time"
    )[:5]

    # ORGANIZE EVENTS BY DATE

    events_by_date = {}

    for event in month_events:

        event_day = event.event_date.day

        if event_day not in events_by_date:

            events_by_date[event_day] = []

        events_by_date[event_day].append(
            event
        )

    # CALENDAR WEEKS

    calendar_obj = pycalendar.Calendar(
        firstweekday=0
    )

    weeks = []

    for week in calendar_obj.monthdatescalendar(
        year,
        month
    ):

        week_days = []

        for day in week:

            week_days.append({
                "date": day,
                "day_number": day.day,
                "in_month": day.month == month,
                "is_today": day == today,

                "events": events_by_date.get(
                    day.day,
                    []
                ) if day.month == month else [],
            })

        weeks.append(
            week_days
        )

    # STATISTICS

    total_events = Event.objects.count()

    events_this_month = month_events.count()

    locations_count = (
        month_events
        .exclude(location="")
        .exclude(location__isnull=True)
        .values("location")
        .distinct()
        .count()
    )

    # PREVIOUS AND NEXT MONTH

    if month == 1:

        previous_date = date(
            year - 1,
            12,
            1
        )

    else:

        previous_date = date(
            year,
            month - 1,
            1
        )

    if month == 12:

        next_date = date(
            year + 1,
            1,
            1
        )

    else:

        next_date = date(
            year,
            month + 1,
            1
        )

    context = {
        "today": today,
        "year": year,
        "month": month,
        "month_label": month_label,
        "weeks": weeks,

        "upcoming_events": upcoming_events,

        "total_events": total_events,
        "events_this_month": events_this_month,
        "locations_count": locations_count,

        "previous_month": previous_date.strftime("%Y-%m"),
        "next_month": next_date.strftime("%Y-%m"),
        "current_month": today.strftime("%Y-%m"),
    }

    return render(
        request,
        "events/calendar.html",
        context
    )


# =====================================================
# SEND INVITATION
# =====================================================

@login_required
def send_invitation(request):

    if request.method == 'POST':

        form = EventInvitationForm(
            request.POST
        )

        if form.is_valid():

            target_type = form.cleaned_data['target_type']

            event = form.cleaned_data['event']

            activity = form.cleaned_data['activity']

            recipient_name = form.cleaned_data['recipient_name']

            organization = form.cleaned_data['recipient_organization']

            emails = form.cleaned_data['recipient_emails']

            message = form.cleaned_data['message']

            if target_type == 'event':

                target = event

                target_name = event.title

                event_date = event.event_date

                start_time = event.start_time

                end_time = event.end_time

                location = event.location

            else:

                target = activity

                target_name = activity.title

                event_date = activity.activity_date

                start_time = activity.start_time

                end_time = activity.end_time

                location = activity.location

            subject = form.cleaned_data['subject'] or (
                f'Official Invitation - {target_name}'
            )

            end_time_text = (
                end_time.strftime('%H:%M')
                if end_time else 'Not specified'
            )

            start_time_text = (
                start_time.strftime('%H:%M')
                if start_time else 'Not specified'
            )

            email_body = f"""
Dear {recipient_name or 'Sir/Madam'},

OJETIL is pleased to invite you to participate in the following event/activity.

Title: {target_name}

Date: {event_date.strftime('%d/%m/%Y')}

Start Time: {start_time_text}

End Time: {end_time_text}

Location: {location}

Organization: {organization or 'OJETIL'}

Message:

{message}

We look forward to your participation.

Best regards,

OJETIL Organization
"""

            sent_count = 0

            failed_count = 0

            for email in emails:

                invitation = EventInvitation.objects.create(
                    event=event if target_type == 'event' else None,

                    activity=activity if target_type == 'activity' else None,

                    recipient_name=recipient_name,

                    recipient_email=email,

                    recipient_organization=organization,

                    subject=subject,

                    message=message,

                    status='Pending'
                )

                try:

                    send_mail(
                        subject=subject,
                        message=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )

                    invitation.status = 'Sent'

                    invitation.sent_at = timezone.now()

                    invitation.save()

                    sent_count += 1

                except Exception as error:

                    invitation.status = 'Failed'

                    invitation.error_message = str(error)

                    invitation.save()

                    failed_count += 1

            if sent_count:

                messages.success(
                    request,
                    f'{sent_count} invitation(s) sent successfully.'
                )

            if failed_count:

                messages.error(
                    request,
                    f'{failed_count} invitation(s) failed to send. '
                    'Check your email configuration.'
                )

            return redirect(
                'events:send_invitation'
            )

    else:

        form = EventInvitationForm()

    invitations = EventInvitation.objects.select_related(
        'event',
        'activity'
    )[:20]

    context = {
        'form': form,

        'invitations': invitations,

        'total_invitations': EventInvitation.objects.count(),

        'sent_invitations': EventInvitation.objects.filter(
            status='Sent'
        ).count(),

        'failed_invitations': EventInvitation.objects.filter(
            status='Failed'
        ).count(),
    }

    return render(
        request,
        'events/send_invitation.html',
        context
    )


@login_required
def invitation_delete(request, pk):
    invitation = get_object_or_404(
        EventInvitation,
        pk=pk
    )

    if request.method == 'POST':
        email = invitation.recipient_email

        invitation.delete()

        messages.success(
            request,
            f'Convite para "{email}" eliminado com sucesso.'
        )

    return redirect('events:send_invitation')
