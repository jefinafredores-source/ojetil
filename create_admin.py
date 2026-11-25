import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ojetil_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ojetil.com', 'admin123')
    print("Admin criado com sucesso!")
else:
    print("Admin ja existe!")