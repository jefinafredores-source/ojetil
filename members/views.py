
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from django.utils import timezone

from .forms import MemberRegistrationForm
from .models import Member
from locations.models import Municipality


# ==================================================
# REGISTU MEMBRU
# ==================================================

def member_register(request):

    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            member = form.save(commit=False)

            # Gera ID Membro automaticamente
            last_member = Member.objects.filter(
                member_id_code__startswith='OJ2026'
            ).order_by('-id').first()

            try:
                last_number = (
                    int(last_member.member_id_code[-4:])
                    if last_member else 0
                )
            except (ValueError, TypeError):
                last_number = 0

            new_number = last_number + 1

            while True:
                new_code = f"OJ2026{new_number:04d}"

                if not Member.objects.filter(
                    member_id_code=new_code
                ).exists():
                    break

                new_number += 1

            member.member_id_code = new_code

            # Membru foun hein aprovasaun
            member.status = 'Em Aprovação'
            member.reviewed_by = None
            member.reviewed_at = None
            member.rejection_reason = None

            member.save()

            messages.success(
                request,
                f'Member {member.full_name} registadu ho susesu. Hein aprovasaun.'
            )

            return redirect('members:list')

        else:
            messages.error(
                request,
                'Erro iha formulário. Favor verifica dadus nebe introduz.'
            )

    else:
        form = MemberRegistrationForm()

    # ID Preview
    last_member = Member.objects.filter(
        member_id_code__startswith='OJ2026'
    ).order_by('-id').first()

    try:
        last_number = (
            int(last_member.member_id_code[-4:])
            if last_member else 0
        )
    except (ValueError, TypeError):
        last_number = 0

    preview_id = f"OJ2026{last_number + 1:04d}"

    municipalities = Municipality.objects.all().order_by('name')

    return render(
        request,
        'members/member_register.html',
        {
            'form': form,
            'preview_id': preview_id,
            'municipalities': municipalities,
        }
    )


# ==================================================
# LISTA MEMBRU + FILTRO
# ==================================================

@login_required
def member_list(request):

    all_members = Member.objects.all()

    members = all_members.select_related(
        'district'
    ).order_by('-created_at')

    # Filtro naran
    search = request.GET.get('search', '').strip()

    if search:
        members = members.filter(full_name__icontains=search)

    # Filtro pozisaun
    selected_position = request.GET.get('position', '').strip()

    if selected_position:
        members = members.filter(position=selected_position)

    # Filtro data rejistu
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    if date_from:
        members = members.filter(registration_date__gte=date_from)

    if date_to:
        members = members.filter(registration_date__lte=date_to)

    # Estatistika
    total_members = all_members.count()

    ativos_count = all_members.filter(status='Ativo').count()
    em_aprovacao_count = all_members.filter(status='Em Aprovação').count()
    inativos_count = all_members.filter(status='Inativo').count()

    # Jeneru
    male_count = all_members.filter(gender='Male').count()
    female_count = all_members.filter(gender='Female').count()
    other_count = all_members.filter(gender='Other').count()

    male_percent = round(
        male_count / total_members * 100
    ) if total_members else 0

    female_percent = round(
        female_count / total_members * 100
    ) if total_members else 0

    context = {
        'members': members,
        'positions': Member.POSITION_CHOICES,
        'search': search,
        'selected_position': selected_position,
        'date_from': date_from,
        'date_to': date_to,

        'total_members': total_members,
        'ativos_count': ativos_count,
        'em_aprovacao_count': em_aprovacao_count,
        'inativos_count': inativos_count,

        'active_members': ativos_count,
        'pending_members': em_aprovacao_count,
        'inactive_members': inativos_count,

        'male_count': male_count,
        'female_count': female_count,
        'other_count': other_count,

        'male_percent': male_percent,
        'female_percent': female_percent,
    }

    return render(
        request,
        'members/member_list.html',
        context
    )


# ==================================================
# DETAIL / VIEW MEMBER
# ==================================================

def member_detail(request, pk):

    member = get_object_or_404(
        Member.objects.select_related(
            'district',
            'place_of_birth'
        ),
        pk=pk
    )

    return render(
        request,
        'members/member_detail.html',
        {'member': member}
    )


# ==================================================
# EDIT MEMBER
# ==================================================

@login_required
@permission_required('members.change_member', raise_exception=True)
def member_edit(request, pk):

    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':

        member.full_name = request.POST.get('full_name')
        member.codigo = request.POST.get('codigo')
        member.phone_number = request.POST.get('phone_number')
        member.email = request.POST.get('email') or None
        member.national_id = request.POST.get('national_id')

        if request.FILES.get('profile_photo'):
            member.profile_photo = request.FILES['profile_photo']

        if request.FILES.get('supporting_document'):
            member.supporting_document = request.FILES['supporting_document']

        member.save()

        messages.success(
            request,
            'Membru atualiza ho susesu.'
        )

        return redirect('members:list')

    return render(
        request,
        'members/member_edit.html',
        {'member': member}
    )


# ==================================================
# DELETE MEMBER
# ==================================================

@login_required
@permission_required('members.delete_member', raise_exception=True)
@require_POST
def member_delete(request, pk):

    member = get_object_or_404(Member, pk=pk)

    member.delete()

    messages.success(
        request,
        'Membru apaga ho susesu.'
    )

    return redirect('members:list')


# ==================================================
# EXPORTAR MEMBRU CSV
# ==================================================

def export_members(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = (
        'attachment; filename="lista_membros_ojetil.csv"'
    )

    response.write('\ufeff')

    writer = csv.writer(response)

    writer.writerow([
        'ID Membro',
        'Nome Completo',
        'Codigo',
        'Posicao',
        'Departamento',
        'Tipo Membro',
        'Status',
        'Data Registo',
    ])

    members = Member.objects.all().order_by('-created_at')

    for member in members:
        writer.writerow([
            member.member_id_code or '-',
            member.full_name,
            member.codigo or '',
            member.position,
            member.department or '',
            member.membership_type,
            member.status,
            (
                member.registration_date.strftime('%Y-%m-%d')
                if member.registration_date else ''
            ),
        ])

    return response


# ==================================================
# IMPORTAR MEMBRU CSV
# ==================================================

def import_members(request):

    if request.method == 'POST' and request.FILES.get('import_file'):

        csv_file = request.FILES['import_file']

        if not csv_file.name.lower().endswith('.csv'):
            messages.error(
                request,
                'Por favor, carregue um ficheiro no formato CSV!'
            )
            return redirect('members:list')

        try:
            file_data = csv_file.read().decode(
                'utf-8-sig'
            ).splitlines()

            reader = csv.DictReader(file_data)

            count = 0

            for row in reader:

                required_fields = [
                    'full_name',
                    'date_of_birth',
                    'national_id',
                    'phone_number',
                    'registration_date',
                ]

                missing_fields = [
                    field for field in required_fields
                    if not row.get(field, '').strip()
                ]

                if missing_fields:
                    messages.error(
                        request,
                        'CSV la kompletu. Falta koluna/dadus obrigatóriu: '
                        + ', '.join(missing_fields)
                    )
                    return redirect('members:list')

                Member.objects.create(
                    full_name=row.get('full_name', '').strip(),
                    date_of_birth=row.get('date_of_birth'),
                    national_id=row.get('national_id', '').strip(),
                    phone_number=row.get('phone_number', '').strip(),
                    registration_date=row.get('registration_date'),
                    codigo=row.get('codigo', '').strip() or None,
                    position=row.get('position', 'Membro'),
                    department=row.get(
                        'department',
                        'Secretariado Geral'
                    ),
                    membership_type=row.get(
                        'membership_type',
                        'Efetivo'
                    ),
                    status=row.get(
                        'status',
                        'Em Aprovação'
                    ),
                    profile_photo='',
                )

                count += 1

            messages.success(
                request,
                f'Importado {count} membru(s) ho susesu!'
            )

        except Exception as error:
            messages.error(
                request,
                f'Erro durante importasaun CSV: {error}'
            )

        return redirect('members:list')

    return redirect('members:list')


# ==================================================
# VERIFICATION AND APPROVAL SYSTEM
# ==================================================

def is_approver(user):

    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name='Presidente').exists()
        )
    )


# ==================================================
# LISTA MEMBRU BA APROVASAUN
# ==================================================

@login_required
@user_passes_test(is_approver)
def member_approval_list(request):

    members = Member.objects.select_related(
        'district'
    ).order_by('-created_at')

    context = {
        'members': members,

        'pending_count': Member.objects.filter(
            status='Em Aprovação'
        ).count(),

        'active_count': Member.objects.filter(
            status='Ativo'
        ).count(),

        'inactive_count': Member.objects.filter(
            status='Inativo'
        ).count(),
    }

    return render(
        request,
        'members/member_approval_list.html',
        context
    )


# ==================================================
# DETAIL MEMBER APPROVAL
# ==================================================

@login_required
@user_passes_test(is_approver)
def member_approval_detail(request, pk):

    member = get_object_or_404(Member, pk=pk)

    return render(
        request,
        'members/member_approval_detail.html',
        {'member': member}
    )


# ==================================================
# APPROVE / REACTIVATE MEMBER
# ==================================================

@login_required
@user_passes_test(is_approver)
@require_POST
def member_approve(request, pk):

    member = get_object_or_404(Member, pk=pk)

    # Permite aprovar membro pendente
    # no ativa fali membro inativo
    if member.status not in ['Em Aprovação', 'Inativo']:

        messages.warning(
            request,
            'Membru nee iha ona status Ativo.'
        )

        return redirect('members:approval_list')

    old_status = member.status

    member.status = 'Ativo'
    member.reviewed_by = request.user
    member.reviewed_at = timezone.now()
    member.rejection_reason = None

    member.save()

    if old_status == 'Inativo':
        messages.success(
            request,
            f'Membru {member.full_name} ativa fali ho susesu!'
        )
    else:
        messages.success(
            request,
            f'Membru {member.full_name} aprova ho susesu!'
        )

    return redirect('members:approval_list')


# ==================================================
# DEACTIVATE MEMBER
# ==================================================

@login_required
@user_passes_test(is_approver)
@require_POST
def member_deactivate(request, pk):

    member = get_object_or_404(Member, pk=pk)

    if member.status != 'Ativo':

        messages.warning(
            request,
            'Membru nee la ativu.'
        )

        return redirect('members:approval_list')

    member.status = 'Inativo'
    member.reviewed_by = request.user
    member.reviewed_at = timezone.now()

    member.save()

    messages.success(
        request,
        f'Membru {member.full_name} desativa ho susesu!'
    )

    return redirect('members:approval_list')


# ==================================================
# REJECT MEMBER
# ==================================================

@login_required
@user_passes_test(is_approver)
@require_POST
def member_reject(request, pk):

    member = get_object_or_404(Member, pk=pk)

    if member.status != 'Em Aprovação':

        messages.warning(
            request,
            'Membru nee la hein aprovasaun.'
        )

        return redirect('members:approval_list')

    reason = request.POST.get(
        'rejection_reason', ''
    ).strip()

    if not reason:

        messages.error(
            request,
            'Favor hatama razaun rejeisaun.'
        )

        return redirect(
            'members:approval_detail',
            pk=member.pk
        )

    member.status = 'Inativo'
    member.reviewed_by = request.user
    member.reviewed_at = timezone.now()
    member.rejection_reason = reason

    member.save()

    messages.success(
        request,
        f'Membru {member.full_name} rejeita ho susesu.'
    )

    return redirect('members:approval_list')


# ==================================================
# MEMBER ID CARDS
# ==================================================

@login_required
def member_id_cards(request):

    if request.method == 'POST':

        selected_ids = request.POST.getlist('members')

        if not selected_ids:

            messages.warning(
                request,
                'Favor hili membru ida ka liu atu gera ID Card.'
            )

            return redirect('members:id_cards')

        selected_members = Member.objects.filter(
            id__in=selected_ids
        ).order_by('full_name')

        return render(
            request,
            'members/id_cards_print.html',
            {
                'members': selected_members,
            }
        )

    members = Member.objects.all().order_by('full_name')

    context = {
        'members': members,
        'total_members': members.count(),
    }

    return render(
        request,
        'members/id_cards.html',
        context
    )
