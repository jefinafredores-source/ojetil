from django.db import models

class Municipality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Municipalities"

class PostoAdministrativo(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='postos')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.municipality.name}"

class Suco(models.Model):
    name = models.CharField(max_length=100)
    posto_administrativo = models.ForeignKey(
        PostoAdministrativo, 
        on_delete=models.CASCADE, 
        null=True,      # Permite valor mamuk iha database
        blank=True      # Permite form mamuk
    )

    def __str__(self):
        return self.name

class Aldeia(models.Model):
    suco = models.ForeignKey(Suco, on_delete=models.CASCADE, related_name='aldeias')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name