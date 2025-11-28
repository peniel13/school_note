from django.db import models

# Create your models here.

class Requete(models.Model):
    TYPE_BIEN_CHOICES = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('hotel', 'Hôtel'),
        ('guesthouse', 'Guesthouse'),
        ('boutique', 'Boutique'),
        ('parcelle vide', 'Parcelle vide'),
        ('terrain agricole', 'Terrain agricole'),
        ('bureau', 'Bureau'),
        ('autres', 'Autres'),
    ]

    nom = models.CharField(max_length=50)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    commune = models.CharField(max_length=100, help_text="Entrez la commune manuellement")
    description = models.TextField()
    type_bien = models.CharField(max_length=50, choices=TYPE_BIEN_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    audio = models.FileField(upload_to='audio/requests/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} - {self.email}"

