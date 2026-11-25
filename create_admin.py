import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ojetil_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# --- USER FOUN ---
USERNAME = 'vanov'
EMAIL = 'support@vanov.tl'
PASSWORD = 'vtlab2026'

user, created = User.objects.get_or_create(username=USERNAME, defaults={'email': EMAIL})
user.email = EMAIL
user.set_password(PASSWORD)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print("Admin vanov kria ona!")
else:
    print("Admin vanov atualiza ona password!")

# --- APAGA USER TUAN ---
User.objects.filter(username='admin').delete()
print("Admin tuan apaga ona!")