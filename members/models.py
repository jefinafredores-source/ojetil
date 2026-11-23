from django.db import models
from locations.models import Municipality
from django.conf import settings

class Member(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    POSITION_CHOICES = [
        ('Membro', 'Membro'),
        ('Estrutura', 'Estrutura'),
        ('Lider', 'Lider'),
        ('Presidente', 'Presidente'),
        ('Presidente Honorário', 'Presidente Honorário'),
        ('Secretario Geral', 'Secretario Geral'),
        ('Secretario Geral Adjunto', 'Secretario Geral Adjunto'),
        ('Diretor', 'Diretor'),
        ('Diretora', 'Diretora'),
    ]

    MEMBERSHIP_TYPE_CHOICES = [
        ('Regular Member', 'Regular Member'),
        ('Honorary Member', 'Honorary Member'),
        ('Fundador', 'Fundador'),
        ('Honorário', 'Honorário'),
        ('Efetivo', 'Efetivo'),
    ]

    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Em Aprovação', 'Em Aprovação'),
        ('Inativo', 'Inativo'),
    ]

        # Verification and Approval Information
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_members',
        verbose_name='Reviewed By'
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Review Date'
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='Rejection Reason'
    )


    # 1. Personal Information
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    codigo = models.CharField(max_length=50, verbose_name='codigo', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male', verbose_name="Gender")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    place_of_birth = models.ForeignKey( Municipality,on_delete=models.SET_NULL,null=True,blank=True,related_name='members_born_here',verbose_name="Local de Nascimento")
    national_id = models.CharField(max_length=17, unique=True, verbose_name="National ID No. / BI")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(unique=True, verbose_name="Email Address", blank=True, null=True)
    address = models.TextField(verbose_name="Address", blank=True, null=True)

    # 2. Organization Information
    member_id_code = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="ID Membro")
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, default='Membro', verbose_name="Position / Role")
    department = models.CharField(max_length=100, default='Secretariado Geral', verbose_name="Departamento", blank=True, null=True)
    district = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, verbose_name="District / Municipality")
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES, default='Regular Member', verbose_name="Membership Type")
    registration_date = models.DateField(verbose_name="Registration Date")

    # 3. Supporting Documents & Photos
    profile_photo = models.ImageField(upload_to='members/photos/', verbose_name="Profile Photo")
    supporting_document = models.FileField(upload_to='members/docs/', blank=True, null=True, verbose_name="Supporting Documents")

    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Em Aprovação')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.member_id_code})"