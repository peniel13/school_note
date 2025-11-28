from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import School
from django.utils.html import format_html

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_ecole', 'annee_scolaire', 'is_active', 'photo_preview', 'date_creation')
    list_filter = ('type_ecole', 'is_active')
    search_fields = ('nom', 'annee_scolaire')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />', obj.photo.url)
        return "—"
    photo_preview.short_description = "Photo"

from django.contrib import admin
from .models import Notation, Matiere

@admin.register(Notation)
class NotationAdmin(admin.ModelAdmin):
    list_display = (
        "eleve_nom",
        "matiere_nom",
        "classe_nom",
        "periode_display",
        "note_attendue",
        "note_obtenue",
        "prof_nom",
        "created_at",
    )

    list_filter = (
        "matiere__prof",
        "matiere__classe",
        "periode_primaire",
        "periode_secondaire",
    )

    search_fields = (
        "eleve__nom",
        "matiere__nom",
        "matiere__classe__nom",
        "matiere__prof__username",
    )

    ordering = ("-created_at",)
    list_per_page = 30

    # Lecture pratique dans la liste
    def eleve_nom(self, obj):
        return obj.eleve.nom
    eleve_nom.short_description = "Élève"

    def matiere_nom(self, obj):
        return obj.matiere.nom
    matiere_nom.short_description = "Matière"

    def classe_nom(self, obj):
        return obj.matiere.classe.nom
    classe_nom.short_description = "Classe"

    def prof_nom(self, obj):
        return obj.matiere.prof.username
    prof_nom.short_description = "Professeur"

    def periode_display(self, obj):
        if obj.periode_primaire:
            return f"Primaire: {obj.periode_primaire.nom}"
        elif obj.periode_secondaire:
            return f"Secondaire: {obj.periode_secondaire.nom}"
        return "—"
    periode_display.short_description = "Période"

    # Optionnel : verrouiller les champs non modifiables une fois créés
    def get_readonly_fields(self, request, obj=None):
        if obj:  # si on édite une notation existante
            return ["eleve", "matiere", "periode_primaire", "periode_secondaire"]
        return []

    # Pré-remplir automatiquement les profs ou classes selon la matière choisie
    def save_model(self, request, obj, form, change):
        # Validation automatique avant sauvegarde
        if obj.periode_primaire and obj.periode_secondaire:
            from django.core.exceptions import ValidationError
            raise ValidationError("Une notation ne peut pas appartenir aux deux périodes.")
        obj.save()


from django.contrib import admin
from .models import BlocMatiere, MaxMatiere
from .forms import BlocMatiereForm, MaxMatiereForm

class MaxMatiereInline(admin.TabularInline):
    model = MaxMatiere
    form = MaxMatiereForm
    extra = 1
    min_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        return formset

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(BlocMatiere)
class BlocMatiereAdmin(admin.ModelAdmin):
    form = BlocMatiereForm
    inlines = [MaxMatiereInline]
    list_display = ("nom", "classe_nom", "school_nom", "total_notes_obtenues", "total_notes_attendues")
    search_fields = ("nom", "classe__nom", "school__nom")
    list_filter = ("school", "classe")
    ordering = ("classe__nom",)

    def classe_nom(self, obj):
        return obj.classe.nom
    classe_nom.short_description = "Classe"

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"


@admin.register(MaxMatiere)
class MaxMatiereAdmin(admin.ModelAdmin):
    form = MaxMatiereForm
    list_display = ("matiere_nom", "bloc_nom", "classe_nom", "note_max", "coefficient")
    search_fields = ("matiere__nom", "bloc__nom", "bloc__classe__nom")
    list_filter = ("bloc__classe", "bloc__school")
    ordering = ("bloc__classe__nom",)

    def bloc_nom(self, obj):
        return obj.bloc.nom
    bloc_nom.short_description = "Bloc"

    def classe_nom(self, obj):
        return obj.bloc.classe.nom
    classe_nom.short_description = "Classe"

    def matiere_nom(self, obj):
        return obj.matiere.nom
    matiere_nom.short_description = "Matière"





from django.contrib import admin
from .models import Eleve, PeriodePrimaire, PeriodeSecondaire, Matiere
from .forms import EleveForm, PeriodePrimaireForm, PeriodeSecondaireForm, MatiereForm


from django.contrib import admin
from .models import Eleve

from django.utils.html import format_html

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    form = EleveForm

    list_display = (
        'nom', 'proprietaire', 'classe_nom', 'school_nom',
        'sexe', 'is_active', 'photo_profil_preview'
    )
    list_filter = ('school', 'classe', 'sexe', 'is_active')
    search_fields = ('nom', 'eleve__email', 'classe__nom', 'school__nom')
    ordering = ('classe__nom', 'nom')

    # Champs affichés dans le formulaire admin
    fields = (
        'school', 'classe', 'nom', 'eleve',
        'sexe', 'image_profil', 'photo_entiere',
        'is_active'
    )

    # 🔥 Aperçu de la photo de profil dans l’admin
    def photo_profil_preview(self, obj):
        if obj.image_profil:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:5px;" />',
                obj.image_profil.url
            )
        return "—"
    photo_profil_preview.short_description = "Photo"

    def classe_nom(self, obj):
        return obj.classe.nom
    classe_nom.short_description = "Classe"

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"

    def proprietaire(self, obj):
        return obj.eleve.email if obj.eleve else "Aucun"
    proprietaire.short_description = "Propriétaire"


# @admin.register(Eleve)
# class EleveAdmin(admin.ModelAdmin):
#     form = EleveForm
#     list_display = ('nom', 'proprietaire', 'classe_nom', 'school_nom', 'is_active')
#     list_filter = ('school', 'classe', 'is_active')
#     search_fields = ('nom', 'eleve__email', 'classe__nom', 'school__nom')
#     ordering = ('classe__nom', 'nom')

#     # Affiche le nom de la classe
#     def classe_nom(self, obj):
#         return obj.classe.nom
#     classe_nom.short_description = "Classe"

#     # Affiche le nom de l'école
#     def school_nom(self, obj):
#         return obj.school.nom
#     school_nom.short_description = "École"

#     # Affiche l'utilisateur (propriétaire)
#     def proprietaire(self, obj):
#         return obj.eleve.email if obj.eleve else "Aucun"
#     proprietaire.short_description = "Propriétaire"



@admin.register(PeriodePrimaire)
class PeriodePrimaireAdmin(admin.ModelAdmin):
    form = PeriodePrimaireForm
    list_display = ('nom', 'school_nom', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('nom', 'school__nom')
    ordering = ('school__nom', 'nom')

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"


@admin.register(PeriodeSecondaire)
class PeriodeSecondaireAdmin(admin.ModelAdmin):
    form = PeriodeSecondaireForm
    list_display = ('nom', 'school_nom', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('nom', 'school__nom')
    ordering = ('school__nom', 'nom')

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    form = MatiereForm
    list_display = ('nom', 'classe_nom', 'prof_nom', 'school_nom')
    list_filter = ('school', 'classe', 'prof')
    search_fields = ('nom', 'classe__nom', 'prof__email', 'school__nom')
    ordering = ('classe__nom', 'nom')

    def classe_nom(self, obj):
        return obj.classe.nom
    classe_nom.short_description = "Classe"

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"

    def prof_nom(self, obj):
        return obj.prof.email if obj.prof else "Aucun"
    prof_nom.short_description = "Professeur"



from django.contrib import admin
from .models import SuperviseurSchool, Classe
from .forms import SuperviseurSchoolForm, ClasseForm


@admin.register(SuperviseurSchool)
class SuperviseurSchoolAdmin(admin.ModelAdmin):
    form = SuperviseurSchoolForm
    list_display = ('superviseur_email', 'school_nom')
    list_filter = ('school',)
    search_fields = ('superviseur__email', 'school__nom')
    ordering = ('school__nom',)

    def superviseur_email(self, obj):
        return obj.superviseur.email
    superviseur_email.short_description = "Superviseur"

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    form = ClasseForm
    list_display = ('nom', 'school_nom', 'titulaire_email', 'type_ecole')
    list_filter = ('school', 'type_ecole')
    search_fields = ('nom', 'school__nom', 'titulaire__email')
    ordering = ('school__nom', 'nom')

    fieldsets = (
        ("Informations de la classe", {
            "fields": ("school", "nom", "type_ecole", "titulaire", "photo_classe")  # ajout photo_classe
        }),
        ("Mot des élèves", {
            "fields": ("mot_des_eleves",),
        }),
    )

    def school_nom(self, obj):
        return obj.school.nom
    school_nom.short_description = "École"

    def titulaire_email(self, obj):
        return obj.titulaire.email if obj.titulaire else "Aucun"
    titulaire_email.short_description = "Titulaire"


# @admin.register(Classe)
# class ClasseAdmin(admin.ModelAdmin):
#     form = ClasseForm
#     list_display = ('nom', 'school_nom', 'titulaire_email', 'type_ecole')
#     list_filter = ('school', 'type_ecole')
#     search_fields = ('nom', 'school__nom', 'titulaire__email')
#     ordering = ('school__nom', 'nom')

#     def school_nom(self, obj):
#         return obj.school.nom
#     school_nom.short_description = "École"

#     def titulaire_email(self, obj):
#         return obj.titulaire.email if obj.titulaire else "Aucun"
#     titulaire_email.short_description = "Titulaire"


from django.contrib import admin
from .models import Maxima
from django.contrib import admin
from .models import Maxima

@admin.register(Maxima)
class MaximaAdmin(admin.ModelAdmin):
    list_display = ('classe', 'get_periode', 'note_attendue', 'cree_par', 'date_creation')
    list_filter = ('classe__school__type_ecole', 'classe__school__nom')
    search_fields = ('classe__nom', 'cree_par__username')
    filter_horizontal = ('matieres',)

    def get_periode(self, obj):
        if obj.periode_primaire:
            return obj.periode_primaire.nom
        elif obj.periode_secondaire:
            return obj.periode_secondaire.nom
        return "-"
    get_periode.short_description = "Période"



from django.contrib import admin
from .models import SemestreTotal, Maxima



from django.contrib import admin
from .models import SemestreTotal
from .forms import SemestreTotalSimpleForm


@admin.register(SemestreTotal)
class SemestreTotalAdmin(admin.ModelAdmin):
    list_display = (
        'classe',
        'school',
        'nom',
        'note_totale_attendue',
        'afficher_matieres',
        'date_creation',
    )
    list_filter = ('classe', 'school', 'date_creation','nom',)
    search_fields = ('classe__nom', 'school__nom')
    readonly_fields = ('note_totale_attendue', 'totaux_matieres', 'date_creation')
    filter_horizontal = ('maximas',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('school', 'classe', 'maximas', 'cree_par')
        }),
        ('Résultats du semestre', {
            'fields': ('note_totale_attendue', 'totaux_matieres')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
        }),
    )

    def afficher_matieres(self, obj):
        """Affiche les matières et leurs totaux dans la liste admin."""
        if not obj.totaux_matieres:
            return "—"
        return ", ".join([f"{k}: {v}" for k, v in obj.totaux_matieres.items()])
    afficher_matieres.short_description = "Totaux par matière"

    def save_model(self, request, obj, form, change):
        """Recalcule automatiquement les totaux à chaque sauvegarde."""
        super().save_model(request, obj, form, change)
        obj.calculer_totaux()


from django.contrib import admin
from .models import Epreuve
from django.contrib import admin
from .models import Epreuve
from .models import NoteEpreuve

class NoteEpreuveInline(admin.TabularInline):
    model = NoteEpreuve
    extra = 0

@admin.register(Epreuve)
class EpreuveAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "matiere",
        "get_school",
        "get_classe",
        "date",
        "note_attendue",
        "get_periode",
    )
    list_filter = (
        "matiere__classe__school",
        "matiere__classe",
        "periode_primaire",
        "periode_secondaire",
        "matiere",
    )
    search_fields = (
        "nom",
        "matiere__nom",
        "matiere__classe__nom",
    )
    ordering = ("-date",)
    list_per_page = 25
    inlines = [NoteEpreuveInline]
    # ----- Méthodes personnalisées -----

    def get_school(self, obj):
        if obj.matiere and obj.matiere.classe and obj.matiere.classe.school:
            return obj.matiere.classe.school.nom
        return "-"
    get_school.short_description = "École"

    def get_classe(self, obj):
        if obj.matiere and obj.matiere.classe:
            return obj.matiere.classe.nom
        return "-"
    get_classe.short_description = "Classe"

    def get_periode(self, obj):
        if obj.periode_primaire:
            return f"{obj.periode_primaire.nom} (Primaire)"
        if obj.periode_secondaire:
            return f"{obj.periode_secondaire.nom} (Secondaire)"
        return "-"
    get_periode.short_description = "Période"





# admin.py

from django.contrib import admin
from .models import NoteEpreuve


@admin.register(NoteEpreuve)
class NoteEpreuveAdmin(admin.ModelAdmin):
    list_display = (
        "epreuve",
        "eleve",
        "get_classe",
        "get_prof",
        "note",
    )
    list_filter = (
        "epreuve__matiere__classe__school",
        "epreuve__matiere__classe",
        "epreuve__matiere",
    )
    search_fields = (
        "epreuve__nom",
        "eleve__nom",
        "epreuve__matiere__nom",
        "epreuve__matiere__classe__nom",
    )
    ordering = ("epreuve",)
    list_per_page = 25

    # ----- Méthodes utiles -----

    def get_classe(self, obj):
        return obj.epreuve.matiere.classe.nom
    get_classe.short_description = "Classe"

    def get_prof(self, obj):
        return obj.epreuve.matiere.prof.get_full_name() if obj.epreuve.matiere.prof else "-"
    get_prof.short_description = "Professeur"



# core/admin.py

from django.contrib import admin
from .models import InfoSchool, InfoSchoolPhoto

# class InfoSchoolPhotoInline(admin.TabularInline):
#     model = InfoSchoolPhoto
#     extra = 3   # afficher 3 champs photos vides par défaut
#     fields = ("image", "caption", "preview")
#     readonly_fields = ("preview",)

#     def preview(self, obj):
#         if obj.image:
#             return f"<img src='{obj.image.url}' width='80' height='80' style='object-fit:cover;border-radius:6px;' />"
#         return "-"
#     preview.allow_tags = True
#     preview.short_description = "Aperçu"


# @admin.register(InfoSchool)
# class InfoSchoolAdmin(admin.ModelAdmin):
#     list_display = (
#         "school",
#         "annee_scolaire",
#         "slogan",
#         "date_created",
#     )
#     list_filter = ("school", "annee_scolaire")
#     search_fields = ("school__nom", "annee_scolaire", "slogan")

#     inlines = [InfoSchoolPhotoInline]

#     fieldsets = (
#         ("Informations générales", {
#             "fields": ("school", "annee_scolaire", "slogan")
#         }),
#         ("Contenu de l'école", {
#             "fields": ("presentation", "mission", "valeurs", "remerciements")
#         }),
#         ("Images", {
#             "fields": ("logo", "image_principale")
#         }),
#         ("Dates", {
#             "fields": ("date_created", "date_updated"),
#             "classes": ("collapse",),
#         }),
#     )

#     readonly_fields = ("date_created", "date_updated")
class InfoSchoolPhotoInline(admin.TabularInline):
    model = InfoSchoolPhoto
    extra = 1
    fields = ("image", "caption")


@admin.register(InfoSchool)
class InfoSchoolAdmin(admin.ModelAdmin):
    list_display = (
        "school",
        "annee_scolaire",
        "slogan",
        "date_created",
    )
    list_filter = ("school", "annee_scolaire")
    search_fields = ("school__nom", "annee_scolaire", "slogan")

    inlines = [InfoSchoolPhotoInline]

    fieldsets = (
        ("Informations générales", {
            "fields": ("school", "annee_scolaire", "slogan")
        }),
        ("Contenu de l'école", {
            "fields": ("presentation", "mission", "valeurs", "remerciements")
        }),
        ("Images principales", {
            "fields": ("logo", "image_principale", "galerie_image")
        }),
        ("Dates", {
            "fields": ("date_created", "date_updated"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("date_created", "date_updated")


@admin.register(InfoSchoolPhoto)
class InfoSchoolPhotoAdmin(admin.ModelAdmin):
    list_display = ('info', 'image', 'caption', 'date_uploaded')
    search_fields = ('info__school__nom', 'info__annee_scolaire', 'caption')

# core/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import FondateurSchool

@admin.register(FondateurSchool)
class FondateurSchoolAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'school', 'photo_preview')
    list_filter = ('school',)
    search_fields = ('nom_complet',)

    readonly_fields = ('photo_preview',)

    fieldsets = (
        ("Informations du fondateur", {
            'fields': (
                'school',
                'nom_complet',
                'biographie',
                'message_annee',
                'vision',
                'photo_profil',
                'photo_preview',
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo_profil:
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;" />',
                obj.photo_profil.url
            )
        return "(Aucune image)"

    photo_preview.short_description = "Aperçu"


# @admin.register(EpreuveNoteObtenue)
# class EpreuveNoteObtenueAdmin(admin.ModelAdmin):
#     list_display = (
#         "nom_epreuve",
#         "matiere",
#         "get_school",
#         "get_classe",
#         "eleve",
#         "date_epreuve",
#         "note_epreuve_attendue",
#         "note_obtenue",
#         "get_periode",
#     )
#     list_filter = (
#         "matiere__classe__school",
#         "periode_primaire",
#         "periode_secondaire",
#         "matiere",
#         "eleve",
#     )
#     search_fields = (
#         "nom_epreuve",
#         "matiere__nom",
#         "matiere__classe__nom",
#         "eleve__nom",
#     )
#     ordering = ("-date_epreuve",)
#     list_per_page = 25

#     def get_school(self, obj):
#         return obj.matiere.classe.school.nom if obj.matiere and obj.matiere.classe and obj.matiere.classe.school else "-"
#     get_school.short_description = "École"

#     def get_classe(self, obj):
#         return obj.matiere.classe.nom if obj.matiere and obj.matiere.classe else "-"
#     get_classe.short_description = "Classe"

#     def get_periode(self, obj):
#         if obj.periode_primaire:
#             return f"{obj.periode_primaire.nom} (Primaire)"
#         elif obj.periode_secondaire:
#             return f"{obj.periode_secondaire.nom} (Secondaire)"
#         return "-"
#     get_periode.short_description = "Période"

# @admin.register(EpreuveNoteObtenue)
# class EpreuveNoteObtenueAdmin(admin.ModelAdmin):
#     list_display = (
#         "nom_epreuve",
#         "matiere",
#         "get_school",
#         "get_classe",
#         "eleve",
#         "date_epreuve",
#         "note_epreuve_attendue",
#         "note_epreuve_obtenue",
#         "get_periode",
#     )
#     list_filter = (
#         "matiere__classe__school",
#         "periode_primaire",
#         "periode_secondaire",
#         "matiere",
#     )
#     search_fields = (
#         "nom_epreuve",
#         "matiere__nom",
#         "matiere__classe__nom",
#         "eleve__nom",
#     )
#     ordering = ("-date_epreuve",)
#     list_per_page = 25

#     def get_school(self, obj):
#         return obj.matiere.classe.school.nom if obj.matiere and obj.matiere.classe and obj.matiere.classe.school else "-"
#     get_school.short_description = "École"

#     def get_classe(self, obj):
#         return obj.matiere.classe.nom if obj.matiere and obj.matiere.classe else "-"
#     get_classe.short_description = "Classe"

#     def get_periode(self, obj):
#         if obj.periode_primaire:
#             return f"{obj.periode_primaire.nom} (Primaire)"
#         elif obj.periode_secondaire:
#             return f"{obj.periode_secondaire.nom} (Secondaire)"
#         return "-"
#     get_periode.short_description = "Période"
