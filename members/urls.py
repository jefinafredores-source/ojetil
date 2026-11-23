
from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # Lista no rejistu membru
    path('', views.member_list, name='list'),
    path('register/', views.member_register, name='register'),
    path('<int:pk>/', views.member_detail, name='detail'),
    path('<int:pk>/edit/', views.member_edit, name='edit'),
    path('<int:pk>/delete/', views.member_delete, name='delete'),

    # Import / Export
    path('export/', views.export_members, name='export'),
    path('import/', views.import_members, name='import'),

    # Verifikasi no Aprovasaun
    path('approval/', views.member_approval_list, name='approval_list'),
    path('approval/<int:pk>/', views.member_approval_detail, name='approval_detail'),
    path('approval/<int:pk>/approve/', views.member_approve, name='approve'),
    path('approval/<int:pk>/deactivate/', views.member_deactivate, name='deactivate'),
    path('approval/<int:pk>/reject/', views.member_reject, name='reject'),

    path('id-cards/', views.member_id_cards, name='id_cards'),
]
