from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('membru/', views.member_report, name='member_report'),
    path('membru/csv/', views.member_report_csv, name='member_report_csv'),
   
    path('export/', views.export_data, name='export_data'),
        
    path('export/download/', views.export_download, name='export_download'),

]
