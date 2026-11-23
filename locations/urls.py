from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    # LIST
    path('municipalities/',
         views.municipality_list_view,
         name='municipality_list'),

    path('postos/',
         views.posto_list_view,
         name='posto_list'),

    path('sucos/',
         views.suco_list_view,
         name='suco_list'),

    path('aldeias/',
         views.aldeia_list_view,
         name='aldeia_list'),

    # MUNICIPALITY CRUD
    path('municipalities/add/',
         views.location_form_view,
         {'location_type': 'municipality'},
         name='municipality_add'),

    path('municipalities/<int:pk>/edit/',
         views.location_form_view,
         {'location_type': 'municipality'},
         name='municipality_edit'),

    path('municipalities/<int:pk>/detail/',
         views.location_detail_view,
         {'location_type': 'municipality'},
         name='municipality_detail'),

    path('municipalities/<int:pk>/delete/',
         views.location_delete_view,
         {'location_type': 'municipality'},
         name='municipality_delete'),

    # POSTO CRUD
    path('postos/add/',
         views.location_form_view,
         {'location_type': 'posto'},
         name='posto_add'),

    path('postos/<int:pk>/edit/',
         views.location_form_view,
         {'location_type': 'posto'},
         name='posto_edit'),

    path('postos/<int:pk>/detail/',
         views.location_detail_view,
         {'location_type': 'posto'},
         name='posto_detail'),

    path('postos/<int:pk>/delete/',
         views.location_delete_view,
         {'location_type': 'posto'},
         name='posto_delete'),

    # SUCO CRUD
    path('sucos/add/',
         views.location_form_view,
         {'location_type': 'suco'},
         name='suco_add'),

    path('sucos/<int:pk>/edit/',
         views.location_form_view,
         {'location_type': 'suco'},
         name='suco_edit'),

    path('sucos/<int:pk>/detail/',
         views.location_detail_view,
         {'location_type': 'suco'},
         name='suco_detail'),

    path('sucos/<int:pk>/delete/',
         views.location_delete_view,
         {'location_type': 'suco'},
         name='suco_delete'),

    # ALDEIA CRUD
    path('aldeias/add/',
         views.location_form_view,
         {'location_type': 'aldeia'},
         name='aldeia_add'),

    path('aldeias/<int:pk>/edit/',
         views.location_form_view,
         {'location_type': 'aldeia'},
         name='aldeia_edit'),

    path('aldeias/<int:pk>/detail/',
         views.location_detail_view,
         {'location_type': 'aldeia'},
         name='aldeia_detail'),

    path('aldeias/<int:pk>/delete/',
         views.location_delete_view,
         {'location_type': 'aldeia'},
         name='aldeia_delete'),
]