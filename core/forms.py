from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model





class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))
    class Meta:
        model= get_user_model()
        fields= ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]




from django import forms
from django.core.exceptions import ValidationError
from .models import Notation, Matiere, Eleve, PeriodePrimaire, PeriodeSecondaire

from django import forms
from django.core.exceptions import ValidationError
from .models import Notation, Eleve

class NotationForm(forms.ModelForm):
    class Meta:
        model = Notation
        fields = [
            "eleve",
            "periode_primaire",
            "periode_secondaire",
            "note_attendue",
            "note_obtenue",
        ]

    def __init__(self, *args, **kwargs):
        prof = kwargs.pop("prof", None)
        classe = kwargs.pop("classe", None)
        super().__init__(*args, **kwargs)

        if classe:
            self.fields["eleve"].queryset = Eleve.objects.filter(classe=classe)

        self.fields["note_attendue"].initial = (
            self.instance.note_attendue if self.instance and self.instance.pk else 0
        )
        self.fields["note_obtenue"].initial = (
            self.instance.note_obtenue if self.instance and self.instance.pk else 0
        )

        self.fields["periode_primaire"].required = False
        self.fields["periode_secondaire"].required = False

    def clean(self):
        cleaned_data = super().clean()
        eleve = cleaned_data.get("eleve")
        periode_primaire = cleaned_data.get("periode_primaire")
        periode_secondaire = cleaned_data.get("periode_secondaire")
        note_attendue = cleaned_data.get("note_attendue")
        note_obtenue = cleaned_data.get("note_obtenue")

        # Empêcher les deux périodes à la fois
        if periode_primaire and periode_secondaire:
            raise ValidationError("Vous ne pouvez pas choisir les deux périodes en même temps.")
        if not periode_primaire and not periode_secondaire:
            raise ValidationError("Veuillez sélectionner une période (primaire ou secondaire).")

        # Vérification que la note obtenue ne dépasse pas la note attendue
        if note_attendue is not None and note_obtenue is not None:
            if note_obtenue > note_attendue:
                raise ValidationError("La note obtenue ne peut pas être supérieure à la note attendue.")

        # On tente de récupérer la matière depuis l'instance (si elle existe)
        matiere = getattr(self.instance, "matiere", None)

        # Vérification des doublons
        if matiere and eleve:
            existing = Notation.objects.filter(
                eleve=eleve,
                matiere=matiere,
                periode_primaire=periode_primaire,
                periode_secondaire=periode_secondaire,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing.exists():
                raise ValidationError("Cette note existe déjà pour cet élève et cette période.")

        return cleaned_data




from django import forms
from .models import BlocMatiere, MaxMatiere, Matiere

class BlocMatiereForm(forms.ModelForm):
    class Meta:
        model = BlocMatiere
        fields = ['school', 'classe', 'nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du bloc (ex: Sciences, Langues, etc.)'}),
            'school': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        classe = cleaned_data.get('classe')
        nom = cleaned_data.get('nom')

        if BlocMatiere.objects.filter(school=school, classe=classe, nom__iexact=nom).exists():
            raise forms.ValidationError("Un bloc avec ce nom existe déjà pour cette classe.")
        return cleaned_data


class MaxMatiereForm(forms.ModelForm):
    class Meta:
        model = MaxMatiere
        fields = ['bloc', 'matiere', 'note_max', 'coefficient']
        widgets = {
            'bloc': forms.Select(attrs={'class': 'form-select'}),
            'matiere': forms.Select(attrs={'class': 'form-select'}),
            'note_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si un bloc est déjà défini, on filtre les matières par classe
        if 'bloc' in self.data:
            try:
                bloc_id = int(self.data.get('bloc'))
                from .models import BlocMatiere
                bloc = BlocMatiere.objects.get(id=bloc_id)
                self.fields['matiere'].queryset = Matiere.objects.filter(classe=bloc.classe)
            except (ValueError, BlocMatiere.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['matiere'].queryset = Matiere.objects.filter(classe=self.instance.bloc.classe)



from django import forms
from django.contrib.auth import get_user_model
from .models import Eleve, PeriodePrimaire, PeriodeSecondaire, Matiere, Classe, School

User = get_user_model()


# --- FORMULAIRE ÉLÈVE ---
class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ["nom", "sexe", "image_profil", "photo_entiere"]
        widgets = {
            "nom": forms.TextInput(attrs={
                'class': 'border rounded px-2 py-1 w-full',
                'placeholder': "Nom de l'élève"
            }),
            "sexe": forms.Select(attrs={
                'class': 'border rounded px-2 py-1 w-full'
            }),
        }

# class EleveForm(forms.ModelForm):
#     class Meta:
#         model = Eleve
#         fields = ["nom", "image_profil", "photo_entiere"]
#         widgets = {
#             "nom": forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full', 'placeholder': "Nom de l'élève"}),
#         }

# --- FORMULAIRE PÉRIODE PRIMAIRE ---
class PeriodePrimaireForm(forms.ModelForm):
    class Meta:
        model = PeriodePrimaire
        fields = ['school', 'nom', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : 1er trimestre'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        nom = cleaned_data.get('nom')

        if school and PeriodePrimaire.objects.filter(school=school, nom__iexact=nom).exists():
            raise forms.ValidationError("Cette période existe déjà pour cette école primaire.")
        return cleaned_data


# --- FORMULAIRE PÉRIODE SECONDAIRE ---
class PeriodeSecondaireForm(forms.ModelForm):
    class Meta:
        model = PeriodeSecondaire
        fields = ['school', 'nom', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : 1er trimestre'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        nom = cleaned_data.get('nom')

        if school and PeriodeSecondaire.objects.filter(school=school, nom__iexact=nom).exists():
            raise forms.ValidationError("Cette période existe déjà pour cette école secondaire.")
        return cleaned_data


# --- FORMULAIRE MATIÈRE ---
class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'prof']   # <-- enlever 'classe'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la matière'}),
            'prof': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prof'].queryset = User.objects.filter(is_active=True)

# class MatiereForm(forms.ModelForm):
#     class Meta:
#         model = Matiere
#         fields = ['classe', 'nom', 'prof']
#         widgets = {
            
#             'classe': forms.Select(attrs={'class': 'form-select'}),
#             'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la matière'}),
#             'prof': forms.Select(attrs={'class': 'form-select'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Filtrer les professeurs actifs
#         self.fields['prof'].queryset = User.objects.filter(is_active=True)

#         # Si une école est sélectionnée, filtrer les classes de cette école
#         if 'school' in self.data:
#             try:
#                 school_id = int(self.data.get('school'))
#                 self.fields['classe'].queryset = Classe.objects.filter(school_id=school_id)
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['classe'].queryset = Classe.objects.filter(school=self.instance.school)



from django import forms
from django.conf import settings
from .models import SuperviseurSchool, Classe, School
from django.contrib.auth import get_user_model

User = get_user_model()


# --- FORMULAIRE SUPERVISEUR ---
class SuperviseurSchoolForm(forms.ModelForm):
    class Meta:
        model = SuperviseurSchool
        fields = ['school', 'superviseur']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select'}),
            'superviseur': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les utilisateurs actifs uniquement
        self.fields['superviseur'].queryset = User.objects.filter(is_active=True)


# --- FORMULAIRE CLASSE ---
from django import forms
from .models import Classe
from django.contrib.auth import get_user_model
from django import forms

from django.forms.widgets import ClearableFileInput
User = get_user_model()

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'titulaire', 'mot_des_eleves', 'photo_classe']  # ajout de photo_classe
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control bg-gray-800 text-white border-gray-600 rounded-md p-2',
                'placeholder': 'Nom de la classe'
            }),
            'titulaire': forms.Select(attrs={
                'class': 'form-select bg-gray-800 text-white border-gray-600 rounded-md p-2'
            }),
            'mot_des_eleves': forms.Textarea(attrs={
                'class': 'form-control bg-gray-800 text-white border-gray-600 rounded-md p-2',
                'rows': 3,
                'placeholder': "Un petit mot des élèves pour cette année (facultatif)"
            }),
            'photo_classe': ClearableFileInput(attrs={
                'class': 'form-control bg-gray-800 text-white border-gray-600 rounded-md p-2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulaire'].queryset = User.objects.filter(is_active=True)
        self.fields['titulaire'].label = "Titulaire (professeur)"
        self.fields['mot_des_eleves'].label = "Mot des élèves"
        self.fields['photo_classe'].label = "Photo de la classe (facultatif)"

# class ClasseForm(forms.ModelForm):
#     class Meta:
#         model = Classe
#         fields = ['nom', 'titulaire']  # ⚠️ pas besoin de 'school' ici
#         widgets = {
#             'nom': forms.TextInput(attrs={
#                 'class': 'form-control bg-gray-800 text-white border-gray-600 rounded-md p-2',
#                 'placeholder': 'Nom de la classe'
#             }),
#             'titulaire': forms.Select(attrs={
#                 'class': 'form-select bg-gray-800 text-white border-gray-600 rounded-md p-2'
#             }),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Filtrer uniquement les utilisateurs actifs
#         self.fields['titulaire'].queryset = User.objects.filter(is_active=True)
#         self.fields['titulaire'].label = "Titulaire (professeur)"


from django import forms
from .models import Maxima

from django import forms
from .models import Maxima, PeriodePrimaire, PeriodeSecondaire, Matiere

# class MaximaForm(forms.ModelForm):
#     class Meta:
#         model = Maxima
#         fields = ['periode_primaire', 'periode_secondaire', 'matieres', 'note_attendue']

#     def __init__(self, *args, **kwargs):
#         # ✅ On récupère la classe et l'école depuis la vue
#         school = kwargs.pop('school', None)
#         classe = kwargs.pop('classe', None)
#         super().__init__(*args, **kwargs)

#         # ✅ Personnalisation du formulaire selon le type d’école
#         if school:
#             if school.type_ecole == 'primaire':
#                 self.fields['periode_primaire'].queryset = PeriodePrimaire.objects.filter(school=school, is_active=True)
#                 self.fields['periode_secondaire'].widget = forms.HiddenInput()
#             elif school.type_ecole == 'secondaire':
#                 self.fields['periode_secondaire'].queryset = PeriodeSecondaire.objects.filter(school=school, is_active=True)
#                 self.fields['periode_primaire'].widget = forms.HiddenInput()

#         # ✅ Matières limitées à la classe actuelle
#         if classe:
#             self.fields['matieres'].queryset = Matiere.objects.filter(classe=classe)

#         # ✅ Style des widgets
#         for field in self.fields.values():
#             field.widget.attrs.update({
#                 'class': 'w-full bg-gray-700 text-white border border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
#             })
class MaximaForm(forms.ModelForm):
    class Meta:
        model = Maxima
        fields = ['periode_primaire', 'periode_secondaire', 'matieres', 'note_attendue']

        # ✅ Widget checkbox pour les matières
        widgets = {
            'matieres': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        # ✅ On récupère la classe et l'école depuis la vue
        school = kwargs.pop('school', None)
        classe = kwargs.pop('classe', None)
        super().__init__(*args, **kwargs)

        # ---------------------------------------
        # ADAPTATION DES PÉRIODES SELON LE TYPE D'ÉCOLE
        # ---------------------------------------
        if school:
            if school.type_ecole == 'primaire':
                self.fields['periode_primaire'].queryset = PeriodePrimaire.objects.filter(
                    school=school, is_active=True
                )
                self.fields['periode_secondaire'].widget = forms.HiddenInput()

            elif school.type_ecole == 'secondaire':
                self.fields['periode_secondaire'].queryset = PeriodeSecondaire.objects.filter(
                    school=school, is_active=True
                )
                self.fields['periode_primaire'].widget = forms.HiddenInput()

        # ---------------------------------------
        # MATIÈRES LIMITÉES À LA CLASSE
        # ---------------------------------------
        if classe:
            self.fields['matieres'].queryset = Matiere.objects.filter(classe=classe)

        # ---------------------------------------
        # STYLE GLOBAL DES WIDGETS
        # (sauf CheckboxSelectMultiple)
        # ---------------------------------------
        for name, field in self.fields.items():
            if name != "matieres":  # ❗ On évite d'appliquer ce style aux checkboxes
                field.widget.attrs.update({
                    'class': 'w-full bg-gray-700 text-white border border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                })


from django import forms
from .models import SemestreTotal, Maxima

from django import forms
from .models import SemestreTotal, Maxima

from django import forms
from .models import SemestreTotal, Maxima

# class SemestreTotalForm(forms.ModelForm):
#     class Meta:
#         model = SemestreTotal
#         fields = ['nom', 'maximas']
#         widgets = {
#             'maximas': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if 'classe' in self.initial:
#             self.fields['maximas'].queryset = Maxima.objects.filter(classe=self.initial['classe'])

from django import forms
from .models import SemestreTotal, Maxima

# class SemestreTotalForm(forms.ModelForm):
#     class Meta:
#         model = SemestreTotal
#         fields = ['school', 'classe']
# forms.py
from django import forms
from .models import SemestreTotal

class SemestreTotalSimpleForm(forms.ModelForm):
    class Meta:
        model = SemestreTotal
        fields = ['nom']  # juste le nom
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white'
            }),
        }

# class AssignMaximaForm(forms.Form):
#     semestre = forms.ModelChoiceField(
#         queryset=None,
#         label="Semestre Total"
#     )
#     maxima = forms.ModelChoiceField(
#         queryset=None,
#         label="Maxima"
#     )

#     def __init__(self, *args, **kwargs):
#         classe = kwargs.pop('classe')
#         super().__init__(*args, **kwargs)

#         # Semestres de cette classe
#         self.fields['semestre'].queryset = SemestreTotal.objects.filter(classe=classe)

#         # Maximas du même school
#         self.fields['maxima'].queryset = Maxima.objects.filter(school=classe.school)
from django import forms
# Assurez-vous d'importer vos modèles ici : SemestreTotal, Maxima

class AssignMaximaForm(forms.Form):
    
    # ⭐ CLASSE INTERNE POUR PERSONNALISER L'AFFICHAGE DU SEMESTRE
    class SemestreTotalChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            # Le format affichera explicitement le nom du Semestre Total (obj.nom)
            # suivi des autres informations que votre __str__ renvoie déjà (e.g. Classe et Total).
            # Cela garantit que le nom du semestre est toujours visible.
            return f"{obj.nom} | {obj.__str__()}"

    semestre = SemestreTotalChoiceField(
        queryset=None,
        label="Semestre Total"
    )
    
    maxima = forms.ModelChoiceField(
        queryset=None,
        label="Maxima"
    )

    def __init__(self, *args, **kwargs):
        # La classe doit être retirée avant d'appeler super().__init__
        classe = kwargs.pop('classe')
        super().__init__(*args, **kwargs)

        # Semestres de cette classe
        self.fields['semestre'].queryset = SemestreTotal.objects.filter(classe=classe)

        # Maximas du même school
        self.fields['maxima'].queryset = Maxima.objects.filter(school=classe.school)


from django import forms
from .models import Epreuve, PeriodePrimaire, PeriodeSecondaire

class EpreuveForm(forms.ModelForm):
    class Meta:
        model = Epreuve
        fields = [
            "nom",
            "date",
            "note_attendue",
            "periode_primaire",
            "periode_secondaire",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        classe = kwargs.pop("classe", None)
        super().__init__(*args, **kwargs)

        # Gestion dynamique des périodes selon le type d'école
        if classe and hasattr(classe.school, "type_ecole"):
            if classe.school.type_ecole == "primaire":
                self.fields["periode_primaire"].queryset = PeriodePrimaire.objects.filter(
                    school=classe.school, is_active=True
                )
                self.fields["periode_secondaire"].widget = forms.HiddenInput()

            else:  # secondaire
                self.fields["periode_secondaire"].queryset = PeriodeSecondaire.objects.filter(
                    school=classe.school, is_active=True
                )
                self.fields["periode_primaire"].widget = forms.HiddenInput()
        else:
            self.fields["periode_primaire"].queryset = PeriodePrimaire.objects.none()
            self.fields["periode_secondaire"].queryset = PeriodeSecondaire.objects.none()

        # Styles uniformes
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 mt-1 text-gray-900 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none",
            })

        # Placeholders
        self.fields["nom"].widget.attrs.update({"placeholder": "Ex : Composition de français"})
        self.fields["note_attendue"].widget.attrs.update({"placeholder": "Ex : 20"})





# forms.py

from django import forms
from .models import NoteEpreuve, Epreuve, Eleve

class NoteEpreuveForm(forms.ModelForm):
    class Meta:
        model = NoteEpreuve
        fields = ["note"]  # on ne montre que la note, pas epreuve ni eleve

    def __init__(self, *args, **kwargs):
        # Récupérer nos arguments personnalisés et les retirer des kwargs
        classe = kwargs.pop("classe", None)
        epreuve = kwargs.pop("epreuve", None)

        super().__init__(*args, **kwargs)

        # Si nécessaire, on pourrait filtrer les élèves, mais ici eleve est fixe
        # donc on ne fait rien pour le champ eleve

        # Si une épreuve est imposée, on n’affiche que le champ note
        if epreuve:
            self.fields["note"].widget.attrs.update({
                "class": "w-full px-3 py-2 mt-1 text-gray-900 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none",
                "placeholder": f"Note pour {epreuve.nom}"
            })


# core/forms.py

from django import forms
from .models import InfoSchool, InfoSchoolPhoto

class InfoSchoolForm(forms.ModelForm):
    class Meta:
        model = InfoSchool
        fields = [
            "school",
            "annee_scolaire",
            "presentation",
            "mission",
            "valeurs",
            "slogan",
            "remerciements",
            "logo",
            "image_principale",
            "galerie_image",
        ]
        widgets = {
            "presentation": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "mission": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "valeurs": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "remerciements": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "annee_scolaire": forms.TextInput(attrs={"class": "form-control"}),
            "slogan": forms.TextInput(attrs={"class": "form-control"}),
        }


# ✔️ Formset pour gérer plusieurs photos en galerie
class InfoSchoolPhotoForm(forms.ModelForm):
    class Meta:
        model = InfoSchoolPhoto
        fields = ["image", "caption"]
        widgets = {
            "caption": forms.TextInput(attrs={"class": "form-control"}),
        }


InfoSchoolPhotoFormSet = forms.inlineformset_factory(
    InfoSchool,
    InfoSchoolPhoto,
    form=InfoSchoolPhotoForm,
    extra=3,         # Nombre de champs image disponibles par défaut
    can_delete=True  # Permet de supprimer des images
)


# core/forms.py

from django import forms
from .models import FondateurSchool

class FondateurSchoolForm(forms.ModelForm):
    class Meta:
        model = FondateurSchool
        fields = [
            'school',
            'nom_complet',
            'biographie',
            'message_annee',
            'vision',
            'photo_profil',
        ]

        widgets = {
            'nom_complet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet du fondateur'
            }),
            'biographie': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Biographie du fondateur'
            }),
            'message_annee': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Message pour l'année scolaire"
            }),
            'vision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Vision du fondateur'
            }),
            'school': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# class EpreuveNoteObtenueForm(forms.ModelForm):
#     class Meta:
#         model = EpreuveNoteObtenue
#         fields = [
#             "nom_epreuve",
#             "date_epreuve",
#             "note_epreuve_attendue",
#             "note_epreuve_obtenue",
#             "periode_primaire",
#             "periode_secondaire",
#         ]
#         widgets = {
#             "date_epreuve": forms.DateInput(attrs={"type": "date"}),
#         }

#     def __init__(self, *args, **kwargs):
#         """
#         On reçoit la classe (primaire ou secondaire) via kwargs pour filtrer les périodes.
#         Exemple d'utilisation :
#             form = EpreuveNoteObtenueForm(classe=classe)
#         """
#         classe = kwargs.pop("classe", None)
#         super().__init__(*args, **kwargs)

#         # Gestion dynamique selon le type d'école
#         if classe and hasattr(classe.school, "type_ecole"):
#             if classe.school.type_ecole == "primaire":
#                 self.fields["periode_primaire"].queryset = PeriodePrimaire.objects.filter(
#                     school=classe.school, is_active=True
#                 )
#                 self.fields["periode_secondaire"].widget = forms.HiddenInput()
#             else:
#                 self.fields["periode_secondaire"].queryset = PeriodeSecondaire.objects.filter(
#                     school=classe.school, is_active=True
#                 )
#                 self.fields["periode_primaire"].widget = forms.HiddenInput()
#         else:
#             # Si aucune classe fournie
#             self.fields["periode_primaire"].queryset = PeriodePrimaire.objects.none()
#             self.fields["periode_secondaire"].queryset = PeriodeSecondaire.objects.none()

#         # Styles uniformes
#         for field in self.fields.values():
#             field.widget.attrs.update({
#                 "class": "w-full px-3 py-2 mt-1 text-gray-900 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none",
#             })

#         # Placeholder pour aider à la saisie
#         self.fields["nom_epreuve"].widget.attrs.update({"placeholder": "Ex : Composition de français"})
#         self.fields["note_epreuve_attendue"].widget.attrs.update({"placeholder": "Ex : 20"})
#         self.fields["note_epreuve_obtenue"].widget.attrs.update({"placeholder": "Laisser vide pour le moment"})
