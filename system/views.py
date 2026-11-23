
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import GeneralSetting, OrganizationProfile
from .forms import GeneralSettingForm, OrganizationProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import UserCreateForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import os
import sqlite3
import tempfile

from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import connection, connections
from django.utils import timezone

from .models import BackupRecord
from .forms import RestoreDatabaseForm

from django.db.models import Q
from django.utils.dateparse import parse_date

from .models import ActivityLog

from django.contrib.auth.models import Group, Permission
from .forms import RoleForm
from django.contrib.contenttypes.models import ContentType

from .forms import AppearanceSettingForm, NotificationSettingForm
from .models import AppearanceSetting, NotificationSetting

@login_required
def system_dashboard(request):
    return render(request, "system/dashboard.html")


@login_required
def general_settings(request):
    setting = GeneralSetting.objects.first()

    if request.method == 'POST':
        form = GeneralSettingForm(
            request.POST,
            request.FILES,
            instance=setting
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'General Settings atualiza ho susesu.'
            )
            return redirect('system:general_settings')
    else:
        form = GeneralSettingForm(instance=setting)

    return render(
        request,
        'system/general_settings.html',
        {'form': form}
    )


@login_required
def organization_profile(request):
    profile = OrganizationProfile.objects.first()

    if request.method == 'POST':
        form = OrganizationProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Organization Profile atualiza ho susesu.'
            )
            return redirect('system:organization_profile')
    else:
        form = OrganizationProfileForm(instance=profile)

    return render(
        request,
        'system/organization_profile.html',
        {'form': form}
    )

# Admin no staff deit bele jere utilizador

# ==================================================
# USER MANAGEMENT - PERMISSIONS
# ==================================================

def is_system_admin(user):
    """
    Admin deit mak bele kria, edita no elimina utilizador.
    """
    return (
        user.is_authenticated and
        (
            user.is_superuser or
            user.is_staff
        )
    )


def is_president(user):
    """
    Presidente bele hare lista utilizador deit.
    """
    return (
        user.is_authenticated and
        user.groups.filter(
            name__in=['President', 'Presidente']
        ).exists()
    )


def can_view_user_management(user):
    """
    Admin no Presidente bele hare lista utilizador.
    """
    return (
        is_system_admin(user) or
        is_president(user)
    )


# ==================================================
# USER LIST - ADMIN + PRESIDENT
# ==================================================

@login_required
@user_passes_test(can_view_user_management)
def user_management(request):

    users = User.objects.all().order_by('-date_joined')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if status == 'active':
        users = users.filter(is_active=True)

    elif status == 'inactive':
        users = users.filter(is_active=False)

    context = {
        'users': users,
        'search': search,
        'status': status,

        'total_users': User.objects.count(),

        'active_users': User.objects.filter(
            is_active=True
        ).count(),

        'inactive_users': User.objects.filter(
            is_active=False
        ).count(),

        # Template uza ida-ne'e atu subar botões
        'can_manage_users': is_system_admin(request.user),
    }

    return render(
        request,
        'system/user_management.html',
        context
    )


# ==================================================
# CREATE USER - ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_system_admin)
def user_create(request):

    if request.method == 'POST':

        form = UserCreateForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Utilizador foun kria ho susesu.'
            )

            return redirect('system:user_management')

    else:
        form = UserCreateForm()

    return render(
        request,
        'system/user_form.html',
        {
            'form': form,
            'title': 'Kria Utilizador Foun',
            'button_text': 'Guardar Utilizador',
        }
    )


# ==================================================
# EDIT USER - ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_system_admin)
def user_edit(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':

        form = UserEditForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Informasaun utilizador atualiza ho susesu.'
            )

            return redirect('system:user_management')

    else:
        form = UserEditForm(instance=user)

    return render(
        request,
        'system/user_form.html',
        {
            'form': form,
            'title': 'Edita Utilizador',
            'button_text': 'Atualiza Utilizador',
            'edit_user': user,
        }
    )


# ==================================================
# DELETE USER - ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_system_admin)
@require_POST
def user_delete(request, pk):

    user = get_object_or_404(User, pk=pk)

    if user == request.user:

        messages.error(
            request,
            'Labele elimina ita nia konta rasik.'
        )

    elif user.is_superuser:

        messages.error(
            request,
            'Labele elimina Superuser.'
        )

    else:

        user.delete()

        messages.success(
            request,
            'Utilizador elimina ho susesu.'
        )

    return redirect('system:user_management')


    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(
            request,
            'Labele elimina ita nia konta rasik.'
        )

    elif user.is_superuser:
        messages.error(
            request,
            'Labele elimina Superuser.'
        )

    else:
        user.delete()

        messages.success(
            request,
            'Utilizador elimina ho susesu.'
        )

    return redirect('system:user_management')



@login_required
def security_settings(request):

    form = PasswordChangeForm(
        user=request.user
    )

    if request.method == 'POST':
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()

            # Mantein session login ativa
            update_session_auth_hash(request, user)

            messages.success(
                request,
                'Password troka ho susesu.'
            )

            return redirect('system:security_settings')

        else:
            messages.error(
                request,
                'Favor verifika password nebe ita hatama.'
            )

    return render(
        request,
        'system/security_settings.html',
        {
            'form': form,
        }
    )


def create_sqlite_backup(request, backup_type='manual'):

    if connection.vendor != 'sqlite':
        raise ValueError('Database laos SQLite.')

    connection.ensure_connection()

    database_path = Path(connection.settings_dict['NAME'])

    if not database_path.exists():
        raise ValueError('Database file la hetan.')

    # SQLite backup API atu evita kopia database ne'ebe sei uza
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.sqlite3',
        delete=False
    )
    temp_path = temp_file.name
    temp_file.close()

    try:
        source = connection.connection
        destination = sqlite3.connect(temp_path)

        try:
            source.backup(destination)
        finally:
            destination.close()

        with open(temp_path, 'rb') as backup:
            filename = (
                f"ojetil_{backup_type}_"
                f"{timezone.now():%Y%m%d_%H%M%S}.sqlite3"
            )

            record = BackupRecord(
                backup_type=backup_type,
                created_by=request.user,
                file_size=os.path.getsize(temp_path)
            )

            record.file.save(
                filename,
                File(backup),
                save=False
            )

            record.save()

        return record

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def backup_restore(request):

    restore_form = RestoreDatabaseForm()

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'backup':

            try:
                record = create_sqlite_backup(request)

                messages.success(
                    request,
                    'Backup database halo ho susesu.'
                )

            except Exception as error:
                messages.error(
                    request,
                    f'Backup falla: {error}'
                )

            return redirect('system:backup_restore')

        elif action == 'restore':

            restore_form = RestoreDatabaseForm(
                request.POST,
                request.FILES
            )

            if restore_form.is_valid():

                uploaded_file = restore_form.cleaned_data[
                    'backup_file'
                ]

                database_path = Path(
                    connection.settings_dict['NAME']
                ).resolve()

                temp_path = None

                try:
                    if connection.vendor != 'sqlite':
                        raise ValueError(
                            'Database laos SQLite.'
                        )

                    if str(database_path) == ':memory:':
                        raise ValueError(
                            'Database memory la suporta restore.'
                        )

                    database_path.parent.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    # Upload backup ba temporary file
                    with tempfile.NamedTemporaryFile(
                        suffix='.sqlite3',
                        dir=database_path.parent,
                        delete=False
                    ) as temp_file:

                        temp_path = temp_file.name

                        for chunk in uploaded_file.chunks():
                            temp_file.write(chunk)

                    # Verifika integridade SQLite
                    test_db = sqlite3.connect(
                        f"file:{temp_path}?mode=ro",
                        uri=True
                    )

                    try:
                        result = test_db.execute(
                            'PRAGMA integrity_check'
                        ).fetchone()

                        if not result or result[0] != 'ok':
                            raise ValueError(
                                'Backup file la validu.'
                            )
                    finally:
                        test_db.close()

                    # Backup seguransa molok restore
                    create_sqlite_backup(
                        request,
                        backup_type='pre_restore'
                    )

                    # Fecha database connection
                    connections.close_all()

                    # Substitui database atual
                    os.replace(
                        temp_path,
                        database_path
                    )

                    temp_path = None

                    connections.close_all()

                    messages.success(
                        request,
                        'Database restaura ho susesu. Favor login fali.'
                    )

                    from django.contrib.auth import logout
                    logout(request)

                    return redirect('login')

                except Exception as error:

                    messages.error(
                        request,
                        f'Restore falla: {error}'
                    )

                finally:
                    if temp_path and os.path.exists(temp_path):
                        os.remove(temp_path)

    records = BackupRecord.objects.all()

    return render(
        request,
        'system/backup_restore.html',
        {
            'records': records,
            'restore_form': restore_form,
        }
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def activity_logs(request):

    logs = ActivityLog.objects.select_related(
        'user'
    ).all()

    search = request.GET.get('search', '').strip()
    action = request.GET.get('action', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if search:
        logs = logs.filter(
            Q(user__username__icontains=search) |
            Q(description__icontains=search) |
            Q(model_name__icontains=search) |
            Q(object_id__icontains=search)
        )

    if action:
        logs = logs.filter(action=action)

    if date_from:
        parsed_from = parse_date(date_from)
        if parsed_from:
            logs = logs.filter(
                created_at__date__gte=parsed_from
            )

    if date_to:
        parsed_to = parse_date(date_to)
        if parsed_to:
            logs = logs.filter(
                created_at__date__lte=parsed_to
            )

    context = {
        'logs': logs[:500],
        'search': search,
        'action': action,
        'date_from': date_from,
        'date_to': date_to,
        'total_logs': ActivityLog.objects.count(),
        'login_count': ActivityLog.objects.filter(
            action='LOGIN'
        ).count(),
        'create_count': ActivityLog.objects.filter(
            action='CREATE'
        ).count(),
        'update_count': ActivityLog.objects.filter(
            action='UPDATE'
        ).count(),
        'delete_count': ActivityLog.objects.filter(
            action='DELETE'
        ).count(),
        'action_choices': ActivityLog.ACTION_CHOICES,
    }

    return render(
        request,
        'system/activity_logs.html',
        context
    )

# ==========================================
# ROLE & PERMISSIONS
# ==========================================

@login_required
@user_passes_test(is_system_admin)
def role_permissions(request):

    groups = Group.objects.prefetch_related(
        'permissions'
    ).order_by('name')

    search = request.GET.get('search', '').strip()

    if search:
        groups = groups.filter(
            name__icontains=search
        )

    if request.method == 'POST':

        form = RoleForm(request.POST)

        if form.is_valid():

            role = form.save()

            messages.success(
                request,
                f"Role '{role.name}' kria ho susesu."
            )

            return redirect('system:role_permissions')

    else:
        form = RoleForm()

    context = {
        'groups': groups,
        'form': form,
        'search': search,
        'total_roles': Group.objects.count(),
        'total_permissions': Permission.objects.count(),
        'total_users': User.objects.count(),
    }

    return render(
        request,
        'system/role_premissions.html',
        context
    )


@login_required
@user_passes_test(is_system_admin)
def role_edit(request, pk):

    role = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':

        form = RoleForm(
            request.POST,
            instance=role
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Role atualiza ho susesu.'
            )

            return redirect('system:role_permissions')

    else:
        form = RoleForm(instance=role)

    return render(
        request,
        'system/role_form.html',
        {
            'form': form,
            'role': role,
            'title': 'Edita Role',
            'button_text': 'Atualiza Role',
        }
    )


@login_required
@user_passes_test(is_system_admin)
@require_POST
def role_delete(request, pk):

    role = get_object_or_404(Group, pk=pk)

    role.delete()

    messages.success(
        request,
        'Role elimina ho susesu.'
    )

    return redirect('system:role_permissions')


@login_required
@user_passes_test(is_system_admin)
def appearance_settings(request):
    setting, created = AppearanceSetting.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = AppearanceSettingForm(request.POST, instance=setting)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Appearance Settings atualiza ho susesu.'
            )
            return redirect('system:appearance_settings')
    else:
        form = AppearanceSettingForm(instance=setting)

    return render(request, 'system/appearance_setting.html', {
        'form': form,
        'setting': setting,
    })


@login_required
@user_passes_test(is_system_admin)
def notifications_settings(request):
    setting, created = NotificationSetting.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = NotificationSettingForm(
            request.POST,
            instance=setting
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Notification Settings atualiza ho susesu.'
            )
            return redirect('system:notifications_settings')
    else:
        form = NotificationSettingForm(instance=setting)

    return render(request, 'system/notifications_setting.html', {
        'form': form,
        'setting': setting,
    })
