
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count

from members.models import Member
from events.models import Activity


# ==========================================
# DASHBOARD HOME
# ==========================================

@login_required
def dashboard_home(request):

    # Estatisticas reais dos membros
    total_members = Member.objects.count()

    # Membros Ativos
    approved_members = Member.objects.filter(
        status='Ativo'
    ).count()

    # Membros aguardando aprovacao
    pending_members = Member.objects.filter(
        status='Em Aprovação'
    ).count()

    # Membros Inativos
    inactive_members = Member.objects.filter(
        status='Inativo'
    ).count()

    # Registos recentes de membros
    recent_registrations = Member.objects.order_by(
        '-created_at'
    )[:5]

    # Atividades recentes (Events app)
    recent_activities = Activity.objects.select_related(
        'category'
    ).order_by('-created_at')[:5]

    # Dados do grafico por municipio
    district_data = (
        Member.objects
        .values('district')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    district_labels = [
        d['district'] if d['district'] else 'La iha'
        for d in district_data
    ]

    district_counts = [
        d['total'] for d in district_data
    ]

    # Dados enviados para o template
    context = {
        'total_members': total_members,
        'approved_members': approved_members,
        'pending_members': pending_members,
        'inactive_members': inactive_members,

        'recent_registrations': recent_registrations,
        'recent_activities': recent_activities,

        'district_labels': district_labels,
        'district_counts': district_counts,
    }

    return render(request, 'dashboard/index.html', context)


# ==========================================
# USER LOGIN
# ==========================================

@ensure_csrf_cookie
def user_login(request):

    # Verificar se utilizador ja iniciou sessao
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            # Iniciar sessao
            login(request, user)

            # Remember me: 14 dias
            if request.POST.get('remember_me'):
                request.session.set_expiry(
                    60 * 60 * 24 * 14
                )
            else:
                request.session.set_expiry(0)

            # Redirecionamento depois login
            next_url = (
                request.POST.get('next')
                or request.GET.get('next')
            )

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)

            return redirect('dashboard:home')

    else:
        form = AuthenticationForm(request)

    return render(request, 'auth/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


# ==========================================
# USER LOGOUT
# ==========================================

@login_required
def user_logout(request):

    logout(request)

    return redirect('dashboard:login')
