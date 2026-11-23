from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from members.models import Member

from .models import (
    Municipality,
    PostoAdministrativo,
    Suco,
    Aldeia
)

from .forms import (
    MunicipalityForm,
    PostoAdministrativoForm,
    SucoForm,
    AldeiaForm
)


# ==================================================
# CONFIGURASAUN CRUD
# ==================================================

LOCATION_CONFIG = {
    'municipality': {
        'model': Municipality,
        'form': MunicipalityForm,
        'title': 'Municipality',
        'list_url': 'locations:municipality_list',
    },
    'posto': {
        'model': PostoAdministrativo,
        'form': PostoAdministrativoForm,
        'title': 'Posto Administrativo',
        'list_url': 'locations:posto_list',
    },
    'suco': {
        'model': Suco,
        'form': SucoForm,
        'title': 'Suco',
        'list_url': 'locations:suco_list',
    },
    'aldeia': {
        'model': Aldeia,
        'form': AldeiaForm,
        'title': 'Aldeia',
        'list_url': 'locations:aldeia_list',
    },
}


# ==================================================
# LIST VIEWS
# ==================================================


def municipality_list_view(request):
    municipalities = Municipality.objects.all()
    total_posto = PostoAdministrativo.objects.count()
    active_members = Member.objects.filter(status='Ativo').count()
    total_members = Member.objects.count()

    context = {
        'municipalities': municipalities,
        'total_municipality': municipalities.count(),
        'total_posto': total_posto,
        'total_members': total_members,
        'active_members': active_members,
    }

    return render(
        request,
        'locations/municipality_management.html',
        context
    )


def posto_list_view(request):
    postos = PostoAdministrativo.objects.select_related( 'municipality').all().order_by('name')
    total_suco = Suco.objects.count()
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='Ativo').count()
    context = {
        'postos': postos,
        'total_posto': postos.count(),
        'total_suco' : total_suco,
        'total_members': total_members,
        'active_members': active_members,
    }

    return render(
        request,
        'locations/posto_management.html',
        context
    )


def suco_list_view(request):
    sucos = Suco.objects.select_related('posto_administrativo','posto_administrativo__municipality').all().order_by('name')
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='Ativo').count()
    context = {
        'sucos': sucos,
        'total_suco': sucos.count(),
        'total_members': total_members,
        'active_members': active_members,
    }

    return render(
        request,
        'locations/suco_management.html',
        context
    )


def aldeia_list_view(request):
    aldeias = Aldeia.objects.select_related('suco','suco__posto_administrativo' ).all().order_by('name')
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='Ativo').count()
    context = {
        'aldeias': aldeias,
        'total_aldeia': aldeias.count(),
        'total_members': total_members,
        'active_members': active_members,
    }

    return render(
        request,
        'locations/aldeia_management.html',
        context
    )


# ==================================================
# ADD / EDIT
# ==================================================

def location_form_view(request, location_type, pk=None):
    config = LOCATION_CONFIG.get(location_type)

    if not config:
        return redirect('locations:municipality_list')

    model = config['model']
    form_class = config['form']

    instance = None

    if pk:
        instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(
            request.POST,
            instance=instance
        )

        if form.is_valid():
            form.save()

            if pk:
                messages.success(
                    request,
                    f'{config["title"]} hadia ho susesu.'
                )
            else:
                messages.success(
                    request,
                    f'{config["title"]} rejista ho susesu.'
                )

            return redirect(config['list_url'])

    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'title': config['title'],
        'is_edit': bool(pk),
        'location_type': location_type,
    }

    return render(
        request,
        'locations/location_form.html',
        context
    )


# ==================================================
# DETAIL
# ==================================================

def location_detail_view(request, location_type, pk):
    config = LOCATION_CONFIG.get(location_type)

    if not config:
        return redirect('locations:municipality_list')

    obj = get_object_or_404(
        config['model'],
        pk=pk
    )

    context = {
        'object': obj,
        'title': config['title'],
        'location_type': location_type,
    }

    return render(
        request,
        'locations/location_detail.html',
        context
    )


# ==================================================
# DELETE
# ==================================================

def location_delete_view(request, location_type, pk):
    config = LOCATION_CONFIG.get(location_type)

    if not config:
        return redirect('locations:municipality_list')

    obj = get_object_or_404(
        config['model'],
        pk=pk
    )

    if request.method == 'POST':
        obj.delete()

        messages.success(
            request,
            f'{config["title"]} elimina ho susesu.'
        )

        return redirect(config['list_url'])

    context = {
        'object': obj,
        'title': config['title'],
        'location_type': location_type,
    }

    return render(
        request,
        'locations/location_confirm_delete.html',
        context
    )