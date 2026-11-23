

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

import csv
from io import BytesIO

from members.models import Member
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def export_member_queryset(request):
    qs = Member.objects.all().order_by('full_name')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if q:
        qs = qs.filter(
            full_name__icontains=q
        ) | qs.filter(
            member_id_code__icontains=q
        )

    if status:
        qs = qs.filter(status=status)

    if date_from:
        qs = qs.filter(
            registration_date__gte=date_from
        )

    if date_to:
        qs = qs.filter(
            registration_date__lte=date_to
        )

    return qs


@login_required
def export_data(request):
    members = export_member_queryset(request)

    return render(request, 'report/export_data.html', {
        'members': members,
        'total_members': Member.objects.count(),
        'total_preview': members.count(),
        'q': request.GET.get('q', ''),
        'status': request.GET.get('status', ''),
        'date_from': request.GET.get('date_from', ''),
        'date_to': request.GET.get('date_to', ''),
    })


@login_required
def export_download(request):
    if request.method != 'POST':
        return redirect('report:export_data')

    qs = export_member_queryset(request)

    # Export ema ne'ebé Admin hili
    selected_ids = request.POST.getlist('selected_ids')

    # Se hili export hotu, uza filtro tomak
    if request.POST.get('export_all') != '1':
        if not selected_ids:
            messages.warning(
                request,
                'Favor hili membru ida antes export.'
            )
            return redirect('report:export_data')

        qs = qs.filter(pk__in=selected_ids)

    if not qs.exists():
        messages.warning(request, 'La iha dadus atu export.')
        return redirect('report:export_data')

    file_format = request.POST.get('file_format', 'xlsx')

    if file_format == 'csv':
        response = HttpResponse(
            content_type='text/csv; charset=utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename="OJETIL_Member_Export.csv"'
        )
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow([
            'No', 'Member ID', 'Full Name',
            'Email', 'Phone', 'Status', 'Registration Date'
        ])

        for i, m in enumerate(qs, start=1):
            writer.writerow([
                i, m.member_id_code, m.full_name,
                m.email, m.phone_number, m.status,
                m.registration_date.strftime('%d/%m/%Y')
                if m.registration_date else ''
            ])

        return response

    if file_format == 'pdf':
        output = BytesIO()

        doc = SimpleDocTemplate(
            output,
            pagesize=landscape(A4)
        )

        styles = getSampleStyleSheet()
        elements = [
            Paragraph('OJETIL - REPORT MEMBRU', styles['Title']),
            Spacer(1, 15)
        ]

        data = [[
            'No', 'Member ID', 'Naran',
            'Email', 'Telefone', 'Status', 'Data Rejistu'
        ]]

        for i, m in enumerate(qs, start=1):
            data.append([
                str(i),
                str(m.member_id_code or '-'),
                str(m.full_name or '-'),
                str(m.email or '-'),
                str(m.phone_number or '-'),
                str(m.status or '-'),
                m.registration_date.strftime('%d/%m/%Y')
                if m.registration_date else '-'
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0B2545')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(table)
        doc.build(elements)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = (
            'attachment; filename="OJETIL_Member_Export.pdf"'
        )
        return response

    # Default: Excel
    if file_format == 'xlsx':
        wb = Workbook()
        ws = wb.active
        ws.title = 'Member Data'

        ws.append([
            'No', 'Member ID', 'Full Name',
            'Email', 'Phone', 'Status', 'Registration Date'
        ])

        for i, m in enumerate(qs, start=1):
            ws.append([
                i, m.member_id_code, m.full_name,
                m.email, m.phone_number, m.status,
                m.registration_date.strftime('%d/%m/%Y')
                if m.registration_date else ''
            ])

        for cell in ws[1]:
            cell.font = __import__('openpyxl').styles.Font(
                bold=True, color='FFFFFF'
            )
            cell.fill = __import__('openpyxl').styles.PatternFill(
                fill_type='solid',
                fgColor='0B2545'
            )

        for column in ws.columns:
            ws.column_dimensions[column[0].column_letter].width = 22

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type=(
                'application/vnd.openxmlformats-officedocument.'
                'spreadsheetml.sheet'
            )
        )
        response['Content-Disposition'] = (
            'attachment; filename="OJETIL_Member_Export.xlsx"'
        )
        return response

    messages.error(request, 'Formatu file la suporta.')
    return redirect('report:export_data')



def get_queryset(request):
    qs = Member.objects.all().order_by('full_name')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Search tuir naran membru
    if q:
        qs = qs.filter(
            full_name__icontains=q
        )

    # Filter tuir status
    if status:
        qs = qs.filter(status=status)

    # Filter tuir data rejistu - hahú
    if date_from:
        qs = qs.filter(
            registration_date__gte=date_from
        )

    # Filter tuir data rejistu - remata
    if date_to:
        qs = qs.filter(
            registration_date__lte=date_to
        )

    return qs


@login_required
def member_report(request):
    qs = get_queryset(request)

    return render(request, 'report/member_report.html', {
        'members': qs,
        'total': qs.count(),
    })


@login_required
def member_report_csv(request):
    qs = get_queryset(request)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8'
    )

    response['Content-Disposition'] = (
        'attachment; filename="report_membru.csv"'
    )

    # Atu Excel lee akentu loos
    response.write('\ufeff')

    writer = csv.writer(response)

    writer.writerow([
        'No',
        'Naran Kompletu',
        'Status',
        'Data Rejistu'
    ])

    for i, m in enumerate(qs, start=1):
        writer.writerow([
            i,
            m.full_name,
            m.status,
            m.registration_date.strftime('%d/%m/%Y')
            if m.registration_date else ''
        ])

    return response
