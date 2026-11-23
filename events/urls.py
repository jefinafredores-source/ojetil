from django.urls import path

from . import views


app_name = 'events'


urlpatterns = [

    # =========================
    # EVENTS
    # =========================

    path('', views.event_list, name='event_list' ),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', views.event_update, name='event_update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),


    # =========================
    # ACTIVITIES
    # =========================

    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/<int:pk>/edit/', views.activity_update, name='activity_update' ),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete' ),


# ========================
# ACTIVITY CATEGORY
# ========================

# Activity Categories
path("categories/", views.activity_category_list, name="activity_category_list"),
path("categories/create/", views.activity_category_create,name="activity_category_create"),
path("categories/<int:pk>/edit/", views.activity_category_update, name="activity_category_update"),
path("categories/<int:pk>/delete/", views.activity_category_delete, name="activity_category_delete"),

# =======================
# CALENDAR
# =======================
path("calendar/", views.calendar_view, name="calendar"),
path('invitations/send/', views.send_invitation, name='send_invitation'),

path(
    'invitations/<int:pk>/delete/',
    views.invitation_delete,
    name='invitation_delete'
),



]