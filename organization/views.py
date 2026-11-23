from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    OrganizationPositionForm,
    OrganizationUnitForm,
    StructureHistoryForm,
)
from .models import OrganizationPosition, OrganizationUnit, StructureHistory


# --- ORGANIZATION STRUCTURE / CHART ---
def organization_structure_view(request):
  root_positions = OrganizationPosition.objects.filter(
      parent__isnull=True, is_active=True
  )
  departments = OrganizationUnit.objects.filter(
      unit_type="department", is_active=True
  )
  committees = OrganizationUnit.objects.filter(
      unit_type="committee", is_active=True
  )
  territorials = OrganizationUnit.objects.filter(
      unit_type="territorial", is_active=True
  )

  context = {
      "root_positions": root_positions,
      "departments": departments,
      "committees": committees,
      "territorials": territorials,
  }
  return render(request, "organization/structure.html", context)

def structure_list_view(request):
    # Foti pozisaun no unit/departamentu ne'ebé iha
    positions = OrganizationPosition.objects.select_related('unit', 'parent').all().order_by('sort_order')
    units = OrganizationUnit.objects.all()
    
    context = {
        'positions': positions,
        'units': units,
    }
    return render(request, 'organization/structure_list.html', context)

# --- DEPARTMENTS CRUD ---
def department_list_view(request):
  departments = OrganizationUnit.objects.filter(unit_type="department")
  context = {
      "departments": departments,
      "total_departments": departments.count(),
      "active_departments": departments.filter(is_active=True).count(),
  }
  return render(request, "organization/departments.html", context)


def department_add_view(request):
  if request.method == "POST":
    form = OrganizationUnitForm(request.POST)
    if form.is_valid():
      dept = form.save(commit=False)
      dept.unit_type = "department"
      dept.save()
      return redirect("organization:departments")
  else:
    form = OrganizationUnitForm(initial={"unit_type": "department"})
  return render(
      request,
      "organization/department_form.html",
      {"form": form, "action": "Add"},
  )

def department_detail_view(request, pk):
    department = get_object_or_404(
        OrganizationUnit,
        pk=pk,
        unit_type="department"
    )

    positions = department.positions.select_related(
        "parent"
    ).all().order_by("sort_order", "title")

    context = {
        "department": department,
        "positions": positions,
        "total_positions": positions.count(),
    }

    return render(
        request,
        "organization/department_detail.html",
        context
    )


def department_edit_view(request, pk):
  dept = get_object_or_404(OrganizationUnit, pk=pk)
  if request.method == "POST":
    form = OrganizationUnitForm(request.POST, instance=dept)
    if form.is_valid():
      form.save()
      return redirect("organization:departments")
  else:
    form = OrganizationUnitForm(instance=dept)
  return render(
      request,
      "organization/department_form.html",
      {"form": form, "action": "Edit"},
  )


def department_delete_view(request, pk):
  dept = get_object_or_404(OrganizationUnit, pk=pk)
  if request.method == "POST":
    dept.delete()
    return redirect("organization:departments")
  return render(request, "organization/confirm_delete.html", {"object": dept})


# --- POSITIONS CRUD ---
def position_list_view(request):
  positions = OrganizationPosition.objects.all()
  context = {
      "positions": positions,
      "total_positions": positions.count(),
      "leadership_count": positions.filter(position_type="leadership").count(),
      "department_count": positions.filter(position_type="department").count(),
  }
  return render(request, "organization/positions.html", context)


def position_add_view(request):
  if request.method == "POST":
    form = OrganizationPositionForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("organization:positions")
  else:
    form = OrganizationPositionForm()
  return render(
      request,
      "organization/position_form.html",
      {"form": form, "action": "Add"},
  )


def position_edit_view(request, pk):
  pos = get_object_or_404(OrganizationPosition, pk=pk)
  if request.method == "POST":
    form = OrganizationPositionForm(request.POST, instance=pos)
    if form.is_valid():
      form.save()
      return redirect("organization:positions")
  else:
    form = OrganizationPositionForm(instance=pos)
  return render(
      request,
      "organization/position_form.html",
      {"form": form, "action": "Edit"},
  )


def position_delete_view(request, pk):
  pos = get_object_or_404(OrganizationPosition, pk=pk)
  if request.method == "POST":
    pos.delete()
    return redirect("organization:positions")
  return render(request, "organization/confirm_delete.html", {"object": pos})




def positional_hierarchy_view(request):
    # Lee pozisaun hotu ne'ebé iha ona iha database
    positions = list(
        OrganizationPosition.objects.select_related(
            "parent", "unit"
        ).order_by("sort_order", "title")
    )

    # Prepara lista oan ba kada pozisaun
    position_map = {p.pk: p for p in positions}
    children_map = {p.pk: [] for p in positions}

    for p in positions:
        p.chart_children = []

    # Organiza pozisaun tuir Parent
    root_positions = []

    for p in positions:
        if p.parent_id in position_map:
            children_map[p.parent_id].append(p)
        else:
            root_positions.append(p)

    visited = set()

    def build_tree(position, path=None):
        if path is None:
            path = set()

        # Prevene loop se iha Parent ne'ebé refere fila ba an rasik
        if position.pk in path:
            return

        visited.add(position.pk)
        current_path = path | {position.pk}

        # Koko evita loop iha hierarkia
        position.chart_children = [
            child
            for child in children_map[position.pk]
            if child.pk not in current_path
        ]

        for child in position.chart_children:
            build_tree(child, current_path)

    # Hahú husi root normal
    for root in root_positions:
        build_tree(root)

    # Se iha pozisaun ne'ebé la hetan root, hatudu nafatin
    # hanesan root baibain atu la sai mamuk
    for p in positions:
        if p.pk not in visited:
            root_positions.append(p)
            build_tree(p)

    context = {
        "positions": positions,
        "root_positions": root_positions,
        "units": OrganizationUnit.objects.all(),
    }

    # Debug: haree dadus iha terminal Django
    print("Total positions:", len(positions))
    print("Total root positions:", len(root_positions))

    return render(
        request,
        "organization/positional_hierarchy.html",
        context,
    )
    positions = list(
        OrganizationPosition.objects.select_related(
            "parent", "unit"
        ).order_by("sort_order", "title")
    )

    # Prepara hierarkia sem altera relasaun iha database
    position_map = {p.pk: p for p in positions}
    children_map = {p.pk: [] for p in positions}

    for p in positions:
        p.chart_children = []

    root_positions = []

    for p in positions:
        if p.parent_id and p.parent_id in position_map:
            children_map[p.parent_id].append(p)
        else:
            root_positions.append(p)

    # Evita loop infinitu se iha relasaun Parent ne'ebé sala
    visited = set()

    def build_tree(position):
        if position.pk in visited:
            position.chart_children = []
            return

        visited.add(position.pk)
        position.chart_children = children_map[position.pk]

        for child in position.chart_children:
            build_tree(child)

    for root in root_positions:
        build_tree(root)

    context = {
        "positions": positions,
        "root_positions": root_positions,
        "units": OrganizationUnit.objects.all(),
    }

    return render(
        request,
        "organization/positional_hierarchy.html",
        context,
    )



# --- COMMITTEES CRUD ---
def committee_list_view(request):
  committees = OrganizationUnit.objects.filter(unit_type="committee")
  context = {
      "committees": committees,
      "total_committees": committees.count(),
      "active_committees": committees.filter(is_active=True).count(),
  }
  return render(request, "organization/committees.html", context)


def committee_add_view(request):
  if request.method == "POST":
    form = OrganizationUnitForm(request.POST)
    if form.is_valid():
      comm = form.save(commit=False)
      comm.unit_type = "committee"
      comm.save()
      return redirect("organization:committees")
  else:
    form = OrganizationUnitForm(initial={"unit_type": "committee"})
  return render(
      request,
      "organization/committee_form.html",
      {"form": form, "action": "Add"},
  )


def committee_edit_view(request, pk):
  comm = get_object_or_404(OrganizationUnit, pk=pk)
  if request.method == "POST":
    form = OrganizationUnitForm(request.POST, instance=comm)
    if form.is_valid():
      form.save()
      return redirect("organization:committees")
  else:
    form = OrganizationUnitForm(instance=comm)
  return render(
      request,
      "organization/committee_form.html",
      {"form": form, "action": "Edit"},
  )


def committee_delete_view(request, pk):
  comm = get_object_or_404(OrganizationUnit, pk=pk)
  if request.method == "POST":
    comm.delete()
    return redirect("organization:committees")
  return render(request, "organization/confirm_delete.html", {"object": comm})


# --- HISTORY CRUD ---
def history_list_view(request):
  histories = StructureHistory.objects.all()
  return render(request, "organization/history.html", {"histories": histories})


def history_add_view(request):
  if request.method == "POST":
    form = StructureHistoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("organization:history")
  else:
    form = StructureHistoryForm()
  return render(
      request, "organization/history_form.html", {"form": form, "action": "Add"}
  )


def history_edit_view(request, pk):
  hist = get_object_or_404(StructureHistory, pk=pk)
  if request.method == "POST":
    form = StructureHistoryForm(request.POST, instance=hist)
    if form.is_valid():
      form.save()
      return redirect("organization:history")
  else:
    form = StructureHistoryForm(instance=hist)
  return render(
      request,
      "organization/history_form.html",
      {"form": form, "action": "Edit"},
  )


def history_delete_view(request, pk):
  hist = get_object_or_404(StructureHistory, pk=pk)
  if request.method == "POST":
    hist.delete()
    return redirect("organization:history")
  return render(request, "organization/confirm_delete.html", {"object": hist})

