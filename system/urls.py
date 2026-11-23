from django.urls import path
from . import views

app_name = "system"

urlpatterns = [
    # ==============================
    # SYSTEM DASHBOARD
    # ==============================
    path(
        "",
        views.system_dashboard,
        name="dashboard"
    ),

    # ==============================
    # GENERAL SETTINGS
    # ==============================
    path(
        "general/",
        views.general_settings,
        name="general_settings"
    ),

    # ==============================
    # ORGANIZATION PROFILE
    # ==============================
    path(
        "organization-profile/",
        views.organization_profile,
        name="organization_profile"
    ),

    # ==============================
    # USER MANAGEMENT
    # ==============================
    path(
        "users/",
        views.user_management,
        name="user_management"
    ),

    path(
        "users/add/",
        views.user_create,
        name="user_create"
    ),

    path(
        "users/<int:pk>/edit/",
        views.user_edit,
        name="user_edit"
    ),

    path(
        "users/<int:pk>/delete/",
        views.user_delete,
        name="user_delete"
    ),

    # ==============================
    # SECURITY
    # ==============================
    path(
        "security/",
        views.security_settings,
        name="security_settings"
    ),

    # ==============================
    # BACKUP AND RESTORE
    # ==============================
    path(
        "backup/",
        views.backup_restore,
        name="backup_restore"
    ),

    # ==============================
    # ACTIVITY LOGS
    # ==============================
    path(
        "activity-logs/",
        views.activity_logs,
        name="activity_logs"
    ),

    # ==============================
    # ROLES AND PERMISSIONS
    # ==============================
    path(
        "roles/",
        views.role_permissions,
        name="role_permissions"
    ),

    path(
        "roles/<int:pk>/edit/",
        views.role_edit,
        name="role_edit"
    ),

    path(
        "roles/<int:pk>/delete/",
        views.role_delete,
        name="role_delete"
    ),

    # ==============================
    # APPEARANCE
    # ==============================
    path(
        "appearance/",
        views.appearance_settings,
        name="appearance_settings"
    ),

    # ==============================
    # NOTIFICATIONS
    # ==============================
    path(
        "notifications/",
        views.notifications_settings,
        name="notifications_settings"
    ),
]