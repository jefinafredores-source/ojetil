
from django.db import models


class OrganizationUnit(models.Model):
    UNIT_TYPES = [
        ("department", "Department"),
        ("committee", "Committee"),
        ("territorial", "Territorial Structure"),
    ]

    name = models.CharField(max_length=150)
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_TYPES,
        default="department",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization Unit"
        verbose_name_plural = "Organization Units"

    def __str__(self):
        return self.name


class OrganizationPosition(models.Model):
    POSITION_TYPES = [
        ("leadership", "Leadership"),
        ("department", "Department"),
        ("consultative", "Consultative"),
    ]

    title = models.CharField(max_length=150)
    position_type = models.CharField(
        max_length=20,
        choices=POSITION_TYPES,
        default="department",
    )
    person_name = models.CharField(max_length=150, blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    unit = models.ForeignKey(
        OrganizationUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="positions",
    )

    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=20, default="#1764ed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "Organization Position"
        verbose_name_plural = "Organization Positions"

    def __str__(self):
        return self.title


class StructureHistory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    change_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-change_date"]
        verbose_name = "Structure History"
        verbose_name_plural = "Structure Histories"

    def __str__(self):
        return self.title
