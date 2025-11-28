from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings 
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Le champ `is_active` est défini par défaut à False
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email



from django.db import models
from django.conf import settings

class School(models.Model):
    nom = models.CharField(max_length=255)
    annee_scolaire = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    TYPE_ECOLE_CHOICES = (
        ('primaire', 'Primaire'),
        ('secondaire', 'Secondaire'),
    )
    type_ecole = models.CharField(max_length=20, choices=TYPE_ECOLE_CHOICES, default='primaire')
    # ✅ Nouveau champ image
    photo = models.ImageField(upload_to='schools/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.type_ecole} - {self.annee_scolaire})"

class InfoSchool(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="infos"
    )

    annee_scolaire = models.CharField(max_length=20)

    presentation = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    valeurs = models.TextField(blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    remerciements = models.TextField(blank=True, null=True)

    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    image_principale = models.ImageField(upload_to='school_images/', blank=True, null=True)

    # 👍 Image de couverture de la galerie
    galerie_image = models.ImageField(
        upload_to='school_info_gallery/',
        blank=True,
        null=True,
        verbose_name="Image de couverture"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('school', 'annee_scolaire')

    def __str__(self):
        return f"{self.school.nom} - Infos {self.annee_scolaire}"


class InfoSchoolPhoto(models.Model):
    info = models.ForeignKey(
        InfoSchool,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    image = models.ImageField(upload_to='school_info_gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo ({self.info.school.nom} - {self.info.annee_scolaire})"


# core/models.py

from django.db import models

class FondateurSchool(models.Model):
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='fondateurs'
    )

    nom_complet = models.CharField(max_length=255)

    biographie = models.TextField(blank=True, null=True)
    message_annee = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)

    photo_profil = models.ImageField(
        upload_to='fondateurs/',
        blank=True,
        null=True
    )

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom_complet']

    def __str__(self):
        return f"{self.nom_complet} - {self.school.nom}"


class SuperviseurSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="superviseurs")
    superviseur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.superviseur.email} supervise {self.school.nom}"

class Classe(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")
    nom = models.CharField(max_length=100)
    titulaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_titulaires"
    )
    type_ecole = models.CharField(max_length=20, blank=True, null=True)

    # 🆕 Nouveau champ
    mot_des_eleves = models.TextField(blank=True, null=True, help_text="Petit message des élèves pour cette année")

    # 🆕 Image de la classe / salle
    photo_classe = models.ImageField(
        upload_to='classes/photos/',
        blank=True,
        null=True,
        help_text="Photo de la classe ou de la salle"
    )

    def save(self, *args, **kwargs):
        if self.school and not self.type_ecole:
            self.type_ecole = self.school.type_ecole
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.school.nom})"

# class Classe(models.Model):
#     school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")
#     nom = models.CharField(max_length=100)
#     titulaire = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="classes_titulaires"
#     )
#     type_ecole = models.CharField(max_length=20, blank=True, null=True)

#     # 🆕 Nouveau champ
#     mot_des_eleves = models.TextField(blank=True, null=True, help_text="Petit message des élèves pour cette année")

#     def save(self, *args, **kwargs):
#         if self.school and not self.type_ecole:
#             self.type_ecole = self.school.type_ecole
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.nom} ({self.school.nom})"



class Eleve(models.Model):
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="eleves")
    nom = models.CharField(max_length=100)

    eleve = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_eleves"
    )

    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="eleves")
    is_active = models.BooleanField(default=True)

    # 🔥 Nouveaux champs ajoutés
    image_profil = models.ImageField(upload_to="eleves/profil/", blank=True, null=True)
    photo_entiere = models.ImageField(upload_to="eleves/complet/", blank=True, null=True)

    # 🔹 Champ sexe
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.nom




class PeriodePrimaire(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="periodes_primaire")
    nom = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} - {self.school.nom} (Primaire)"


class PeriodeSecondaire(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="periodes_secondaire")
    nom = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} - {self.school.nom} (Secondaire)"



class Matiere(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="matieres")
    nom = models.CharField(max_length=100)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="matieres")
    prof = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="matieres")

    def __str__(self):
        return f"{self.nom} ({self.classe.nom})"


from django.db.models import Sum

class BlocMatiere(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="blocs_matieres")
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name="blocs_matieres")
    nom = models.CharField(max_length=100)

    def total_notes_obtenues(self):
        total = 0
        for max_matiere in self.max_matieres.all():
            somme = max_matiere.matiere.notations.aggregate(total=Sum('note_obtenue'))['total']
            if somme:
                total += somme
        return total

    def total_notes_attendues(self):
        total = 0
        for max_matiere in self.max_matieres.all():
            somme = max_matiere.matiere.notations.aggregate(total=Sum('note_attendue'))['total']
            if somme:
                total += somme
        return total

    def __str__(self):
        return f"{self.nom} ({self.classe.nom})"
    class Meta:
          unique_together = ('classe', 'nom')


class MaxMatiere(models.Model):
    bloc = models.ForeignKey(BlocMatiere, on_delete=models.CASCADE, related_name="max_matieres")
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE, related_name="max_values")
    note_max = models.FloatField(default=20)
    coefficient = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.matiere.nom} ({self.bloc.nom}) - Max: {self.note_max}, Coef: {self.coefficient}"



class Notation(models.Model):
    eleve = models.ForeignKey("Eleve", on_delete=models.CASCADE, related_name="notations")
    matiere = models.ForeignKey("Matiere", on_delete=models.CASCADE, related_name="notations")

    # Périodes (primaire ou secondaire)
    periode_primaire = models.ForeignKey(
        "PeriodePrimaire", on_delete=models.CASCADE, null=True, blank=True, related_name="notations_primaire"
    )
    periode_secondaire = models.ForeignKey(
        "PeriodeSecondaire", on_delete=models.CASCADE, null=True, blank=True, related_name="notations_secondaire"
    )

    note_attendue = models.FloatField()
    note_obtenue = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        periode_name = (
            self.periode_primaire.nom if self.periode_primaire
            else (self.periode_secondaire.nom if self.periode_secondaire else "Aucune période")
        )
        return f"{self.eleve.nom} - {self.matiere.nom} ({periode_name})"

    def clean(self):
        # Validation logique
        if self.periode_primaire and self.periode_secondaire:
            raise ValidationError("Une notation ne peut pas appartenir aux deux périodes à la fois.")
        if not self.periode_primaire and not self.periode_secondaire:
            raise ValidationError("Une notation doit appartenir à au moins une période.")



# class Maxima(models.Model):
#     school = models.ForeignKey(
#         School, on_delete=models.CASCADE, related_name="maximas"
#     )
#     classe = models.ForeignKey(
#         Classe, on_delete=models.CASCADE, related_name="maximas"
#     )
#     periode_primaire = models.ForeignKey(
#         PeriodePrimaire,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="maximas_primaire"
#     )
#     periode_secondaire = models.ForeignKey(
#         PeriodeSecondaire,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="maximas_secondaire"
#     )
#     matieres = models.ManyToManyField(
#         Matiere,
#         related_name="maximas",
#         help_text="Sélectionnez les matières concernées par cette note maximale"
#     )
#     note_attendue = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         help_text="Note maximale attendue (ex: 50)"
#     )
#     cree_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="maximas_crees"
#     )
#     date_creation = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = "Maximas"
#         ordering = ["-date_creation"]

#     def __str__(self):
#         periode = (
#             self.periode_primaire.nom
#             if self.periode_primaire
#             else self.periode_secondaire.nom
#             if self.periode_secondaire
#             else "Période non définie"
#         )
#         return f"{self.classe.nom} - {periode} (Max: {self.note_attendue})"
class Maxima(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="maximas"
    )
    classe = models.ForeignKey(
        Classe, on_delete=models.CASCADE, related_name="maximas"
    )
    periode_primaire = models.ForeignKey(
        PeriodePrimaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maximas_primaire"
    )
    periode_secondaire = models.ForeignKey(
        PeriodeSecondaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maximas_secondaire"
    )
    matieres = models.ManyToManyField(
        Matiere,
        related_name="maximas",
        help_text="Sélectionnez les matières concernées par cette note maximale"
    )
    note_attendue = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Note maximale attendue (ex: 50)"
    )
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maximas_crees"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Maximas"
        ordering = ["-date_creation"]

    def __str__(self):
        periode = (
            self.periode_primaire.nom
            if self.periode_primaire
            else self.periode_secondaire.nom
            if self.periode_secondaire
            else "Période non définie"
        )
        return f"{self.classe.nom} - {periode} (Max: {self.note_attendue})"

    @property
    def periode(self):
        """Renvoie le nom de la période (primaire ou secondaire)"""
        if self.periode_primaire:
            return self.periode_primaire.nom
        if self.periode_secondaire:
            return self.periode_secondaire.nom
        return "Période non définie"


from django.db import models
from django.conf import settings
from decimal import Decimal

from django.db import models
from django.conf import settings
from decimal import Decimal

class SemestreTotal(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="semestres_totaux")
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name="semestres_totaux")
    maximas = models.ManyToManyField('Maxima', related_name="semestres_totaux")

    nom = models.CharField(max_length=100, blank=True)  # <-- nouveau champ pour nom du semestre

    note_totale_attendue = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    totaux_matieres = models.JSONField(default=dict, blank=True)

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="semestres_totaux_crees"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Total du Semestre"
        verbose_name_plural = "Totaux des Semestres"

    def __str__(self):
        return f"{self.classe.nom} - Total: {self.note_totale_attendue}"

    def calculer_totaux(self):
        total_general = 0
        totaux_par_matiere = {}

        for maxima in self.maximas.all():
            total_general += float(maxima.note_attendue)
            for matiere in maxima.matieres.all():
                if matiere.nom not in totaux_par_matiere:
                    totaux_par_matiere[matiere.nom] = 0
                totaux_par_matiere[matiere.nom] += float(maxima.note_attendue)

        self.note_totale_attendue = total_general
        self.totaux_matieres = totaux_par_matiere
        self.save()




class Epreuve(models.Model):
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    date = models.DateField()
    note_attendue = models.FloatField()   # ← ajouté ici (ancien "maximum")

    # période (primaire OU secondaire)
    periode_primaire = models.ForeignKey(
        'PeriodePrimaire', null=True, blank=True, on_delete=models.SET_NULL
    )
    periode_secondaire = models.ForeignKey(
        'PeriodeSecondaire', null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.nom} - {self.matiere.nom}"


class NoteEpreuve(models.Model):
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE, related_name='notes')
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='notes_epreuves')
    note = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('epreuve', 'eleve')

    def __str__(self):
        return f"{self.eleve.nom} - {self.epreuve.nom} : {self.note or 'Non rempli'}"


# class EpreuveNoteObtenue(models.Model):
#     matiere = models.ForeignKey(
#         'Matiere', on_delete=models.CASCADE, related_name='epreuves'
#     )
#     nom_epreuve = models.CharField(max_length=255)
#     date_epreuve = models.DateField()
#     note_epreuve_attendue = models.FloatField()
#     eleve = models.ForeignKey(
#         'Eleve', on_delete=models.CASCADE, related_name='notes_epreuves'
#     )
#     note_obtenue = models.FloatField(null=True, blank=True)  # remplie plus tard
#     periode_primaire = models.ForeignKey(
#         'PeriodePrimaire', null=True, blank=True, on_delete=models.SET_NULL
#     )
#     periode_secondaire = models.ForeignKey(
#         'PeriodeSecondaire', null=True, blank=True, on_delete=models.SET_NULL
#     )

#     class Meta:
#         unique_together = ('nom_epreuve', 'eleve', 'matiere', 'periode_primaire', 'periode_secondaire')
#         # Empêche d'avoir plusieurs notes pour le même élève et la même épreuve

#     def __str__(self):
#         return f"{self.nom_epreuve} - {self.matiere.nom} - {self.eleve.nom}"


# class NoteEpreuve(models.Model):
#     epreuve = models.ForeignKey(EpreuveNoteObtenue, on_delete=models.CASCADE, related_name='notes')
#     eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='notes_epreuves')
#     note_obtenue = models.FloatField(null=True, blank=True)

#     class Meta:
#         unique_together = ('epreuve', 'eleve')  # Un élève ne peut avoir qu'une note par épreuve

#     def __str__(self):
#         return f"{self.eleve.nom} - {self.epreuve.nom_epreuve} : {self.note_obtenue or 'Non rempli'}"

# class EpreuveNoteObtenue(models.Model):
#     matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE, related_name='epreuves')
#     nom_epreuve = models.CharField(max_length=255)
#     date_epreuve = models.DateField()
#     note_epreuve_attendue = models.FloatField()
#     note_epreuve_obtenue = models.FloatField(null=True, blank=True)  # remplie plus tard
#     periode_primaire = models.ForeignKey('PeriodePrimaire', null=True, blank=True, on_delete=models.SET_NULL)
#     periode_secondaire = models.ForeignKey('PeriodeSecondaire', null=True, blank=True, on_delete=models.SET_NULL)
#     eleve = models.ForeignKey('Eleve', null=True, blank=True, on_delete=models.CASCADE, related_name='notes_epreuves')

#     def __str__(self):
#         return f"{self.nom_epreuve} - {self.matiere.nom}"


# from django.db import models
# from django.conf import settings
# from django.core.exceptions import ValidationError

# class EpreuveNoteObtenue(models.Model):
#     notation = models.ForeignKey(
#         "Notation",
#         on_delete=models.CASCADE,
#         related_name="epreuves"
#     )
#     nom_epreuve = models.CharField(max_length=100)
#     date_epreuve = models.CharField(
#         max_length=100,
#         help_text="Ex: '12 octobre 2025' ou 'Semaine 3 du trimestre'"
#     )
#     note_epreuve_attendue = models.FloatField()
#     note_epreuve_obtenue = models.FloatField()

#     # Champs de période (primaire ou secondaire)
#     periode_primaire = models.ForeignKey(
#         "PeriodePrimaire",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="epreuves_primaire"
#     )
#     periode_secondaire = models.ForeignKey(
#         "PeriodeSecondaire",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="epreuves_secondaire"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Épreuve Note Obtenue"
#         verbose_name_plural = "Épreuves Notes Obtenues"
#         ordering = ["-created_at"]

#     def __str__(self):
#         periode_name = (
#             self.periode_primaire.nom if self.periode_primaire
#             else self.periode_secondaire.nom if self.periode_secondaire
#             else "Aucune période"
#         )
#         return f"{self.nom_epreuve} - {self.notation.eleve.nom} ({periode_name})"

#     def clean(self):
#         # Validation : ne pas avoir les deux périodes à la fois
#         if self.periode_primaire and self.periode_secondaire:
#             raise ValidationError("Une épreuve ne peut pas appartenir aux deux périodes à la fois.")
#         if not self.periode_primaire and not self.periode_secondaire:
#             raise ValidationError("Une épreuve doit appartenir à au moins une période.")
