
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard, Login no Logout
    path('', include('dashboard.urls')),

    # Members
    path('members/', include('members.urls')),

    # Locations
    path('locations/', include('locations.urls')),

    # Events
    path('events/', include('events.urls')),

    # Organization
    path('organization/', include('organization.urls')),

    # Reports
    path('report/', include('reports.urls')),

    # System Settings
    path('system/', include('system.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
