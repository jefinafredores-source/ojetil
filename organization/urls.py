from django.urls import path
from . import views

app_name = "organization"

# Prefix "organization/" mai husi urls.py projetu:
#   path("organization/", include("organization.urls"))
# Entaun iha ne'e la presiza hakerek "organization/" fali.
urlpatterns = [
    # Chart & list
    path("", views.organization_structure_view, name="structure"),
    path("structure-list/", views.structure_list_view, name="structure_list"),
# Departments
path("departments/", views.department_list_view, name="departments"),
path("departments/add/", views.department_add_view, name="department_add"),
path("departments/<int:pk>/detail/",views.department_detail_view,name="department_detail"),
path("departments/<int:pk>/edit/", views.department_edit_view, name="department_edit"),
path("departments/<int:pk>/delete/", views.department_delete_view, name="department_delete"),

    # Positions
    path("positions/", views.position_list_view, name="positions"),
    path("positions/add/", views.position_add_view, name="position_add"),
    path("positions/<int:pk>/edit/", views.position_edit_view, name="position_edit"),
    path("positions/<int:pk>/delete/", views.position_delete_view, name="position_delete"),
    
path("positional-hierarchy/", views.positional_hierarchy_view, name="positional_hierarchy"),


    # Committees
    path("committees/", views.committee_list_view, name="committees"),
    path("committees/add/", views.committee_add_view, name="committee_add"),
    path("committees/<int:pk>/edit/", views.committee_edit_view, name="committee_edit"),
    path("committees/<int:pk>/delete/", views.committee_delete_view, name="committee_delete"),

    # History
    path("history/", views.history_list_view, name="history"),
    path("history/add/", views.history_add_view, name="history_add"),
    path("history/<int:pk>/edit/", views.history_edit_view, name="history_edit"),
    path("history/<int:pk>/delete/", views.history_delete_view, name="history_delete"),
]