from django.urls import path
from . import views 

urlpatterns = [
    
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('signout',views.signout, name='signout'),
    path('profile',views.profile, name='profile'),
    path('update_profile',views.update_profile, name='update_profile'),
    path('user/school/<int:pk>/', views.school_detail, name='school_detail'),
    path("school/classe/<int:classe_id>/update-titulaire/", views.update_titulaire, name="update_titulaire"),
    path('classe/<int:classe_id>/', views.classe_detail, name='classe_detail'),
    path('eleve/delete/<int:eleve_id>/', views.delete_eleve, name='delete_eleve'),
    path('matiere/<int:matiere_id>/', views.matiere_detail, name='matiere_detail'),
    path('matiere/<int:matiere_id>/periode/<int:periode_id>/', views.periode_detail, name='periode_detail'),
    path('notation/<int:notation_id>/modifier/', views.modifier_notation, name='modifier_notation'),
    path('notation/<int:notation_id>/supprimer/', views.supprimer_notation, name='supprimer_notation'),
    path('eleves/<int:eleve_id>/', views.details_eleve, name='details_eleve'),
    path('eleves/<int:eleve_id>/periode/<int:periode_id>/', views.details_periode, name='details_periode'),
    path('eleve/<int:eleve_id>/', views.situations_eleve, name='situations_eleve'),
    path('bulletin/<int:eleve_id>/', views.bulletin_eleve, name='bulletin_eleve'),
    # path('b/<int:eleve_id>/', views.bulletin_branche, name='bulletin_eleve'),
    path('',views.control, name= 'control'),
    path('schools/<int:school_id>/classes/', views.classes_list, name='classes_list'),
    path('schools/<int:school_id>/eleves/', views.eleves_list, name='eleves_list'),
    path('schools/<int:school_id>/professeurs/', views.professeurs_list, name='professeurs_list'),
    path('classe/<int:classe_id>/maxima/', views.creer_maxima, name='creer_maxima'),
    path(
        'classe/<int:classe_id>/semestres/',
        views.definir_semestre_total,
        name='definir_semestre_total'
    ),
    path(
        'classe/<int:classe_id>/semestres/<int:semestre_id>/modifier/',
        views.definir_semestre_total,
        {'action': 'modifier'},
        name='modifier_semestre_total'
    ),

    # Détail d’un semestre total
    path(
        'semestre/<int:pk>/',
        views.detail_semestre_total,
        name='detail_semestre_total'
    ),
    path('classe/<int:classe_id>/assigner-eleve/', views.assigner_eleve, name='assigner_eleve'),
    path("classe/<int:classe_id>/creation-matiere/", views.creer_matiere_classe, name="creer_matiere_classe"),
    path('bulletin/<int:eleve_id>/pdf/', views.bulletin_eleve_pdf, name='bulletin_eleve_pdf'),
    path('bulletin/excel/<int:eleve_id>/', views.bulletin_eleve_excel, name='bulletin_eleve_excel'), # 🎯 Nouvelle URL # 🎯 Nouvelle URL
    path('periode/<int:periode_id>/pdf/', views.generer_pdf, name='generer_pdf'),
    path('eleves/<int:eleve_id>/periode/<int:periode_id>/pdf/', views.periode_eleve_pdf, name='periode_eleve_pdf'),
    path('matiere/<int:matiere_id>/periode/<int:periode_id>/pdf/', views.liste_notation_pdf, name='liste_notation_pdf'),
    path('matiere/<int:matiere_id>/epreuves/<int:periode_id>/', views.detail_epreuve, name='detail_epreuve'),
    path(
        'eleve/<int:eleve_id>/matiere/<int:matiere_id>/periode/<int:periode_id>/epreuves/',
        views.detail_epreuve_eleve,
        name='detail_epreuve_eleve'
    ),
    path('school/<int:school_id>/souvenir-pdf/', views.souvenir_school_pdf, name='souvenir_school_pdf'),
    path('souvenir/eleve/<int:eleve_id>/', views.souvenir_eleve_pdf, name='souvenir_eleve_pdf'),
    path('school/<int:school_id>/info/', views.info_school_detail, name='info_school_detail'),
    path('user/school/<int:school_id>/fondateur/', views.fondateur_school_view, name='fondateur_school'),
    path('admin/schools/', views.school_list_view, name='school_list'),
    path('semestre-total/', views.semestre_total_crud, name='semestre_total_crud'),
    path('classe/<int:classe_id>/assigner-maxima/', views.assigner_maxima, name='assigner_maxima'),
    path(
    'user/classe/<int:classe_id>/semestres/<int:semestre_id>/supprimer/',
    views.supprimer_semestre_total,
    name='supprimer_semestre_total'
       ),


    # path('schools/<int:school_id>/eleves/', views.eleves_list, name='eleves_list'),
    # path('schools/<int:school_id>/profs/', views.profs_list, name='profs_list'),
]