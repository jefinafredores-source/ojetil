
from django.db import models


class GeneralSetting(models.Model):
    site_name = models.CharField(
        max_length=150,
        default="OJETIL"
    )
    site_description = models.TextField(
        blank=True
    )
    contact_email = models.EmailField(
        blank=True
    )
    contact_phone = models.CharField(
        max_length=30,
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    logo = models.ImageField(
        upload_to="system/logo/",
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "General Setting"
        verbose_name_plural = "General Settings"

    def __str__(self):
        return self.site_name


class OrganizationProfile(models.Model):
    organization_name = models.CharField(
        max_length=150,
        default="OJETIL"
    )
    abbreviation = models.CharField(
        max_length=30,
        blank=True
    )
    vision = models.TextField(
        blank=True
    )
    mission = models.TextField(
        blank=True
    )
    history = models.TextField(
        blank=True
    )
    email = models.EmailField(
        blank=True
    )
    phone = models.CharField(
        max_length=30,
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Organization Profile"
        verbose_name_plural = "Organization Profile"

    def __str__(self):
        return self.organization_name


class BackupRecord(models.Model):

    BACKUP_TYPES = [
        ('manual', 'Manual Backup'),
        ('pre_restore', 'Before Restore'),
    ]

    file = models.FileField(
        upload_to='system_backups/'
    )

    backup_type = models.CharField(
        max_length=20,
        choices=BACKUP_TYPES,
        default='manual'
    )

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    file_size = models.PositiveBigIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Backup Record'
        verbose_name_plural = 'Backup Records'

    def __str__(self):
        return f"Backup {self.created_at:%Y-%m-%d %H:%M}"

class ActivityLog(models.Model):

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('BACKUP', 'Backup'),
        ('RESTORE', 'Restore'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='system_activity_logs'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    object_id = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        username = self.user.username if self.user else 'Unknown'
        return f'{username} - {self.action} - {self.created_at}'
    
    
class AppearanceSetting(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    ]

    SIDEBAR_CHOICES = [
        ('dark', 'Dark Sidebar'),
        ('light', 'Light Sidebar'),
    ]

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='light'
    )
    sidebar_style = models.CharField(
        max_length=20,
        choices=SIDEBAR_CHOICES,
        default='dark'
    )
    primary_color = models.CharField(
        max_length=20,
        default='#0d6efd'
    )
    compact_mode = models.BooleanField(default=False)
    show_logo = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Appearance Settings"


class NotificationSetting(models.Model):
    email_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)

    notify_new_member = models.BooleanField(default=True)
    notify_member_status = models.BooleanField(default=True)
    notify_new_event = models.BooleanField(default=True)
    notify_backup = models.BooleanField(default=True)
    notify_security = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Notification Settings"
