from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls import include as include_url

urlpatterns = [
	path('', views.accueil, name="accueil_page"),
	path('enregistrer/', views.enregistrer, name="enregistrer_page"),
	path('enregistrement/', views.enregistrement, name="enregistrement_processus"),
	path('verifier/', views.verifier, name="verifier_page"),
	path('verifier_process/', views.verifier_process, name="verifier_process"),
	path('reenvoyer_code/', views.reenvoyer_code, name="reenvoyer_code_process"),
	path('connexion/', views.connexion, name="connexion_page"),
	path('connexion_p', views.connexion_p, name="connexion_processus"),
	path('mdp_email/', views.mdp_email, name="mdp_email_page"),
	path('mdp_pass/', views.mdp_pass, name="mdp_pass_page"),
	path('mdp_verifier/<int:user_id>', views.mdp_verifier, name="mdp_verifier_process"),
	path('vendre/', views.vendre, name="vendre_page"),
	path('deconexion/', views.deconnexion, name="deconnexion_processus"),
	path('nouvelle_annonce/', views.nouvelle_annonce, name="nouvelle_annonce_page"),
	path('nouvelle_annonce_processus', views.nouvelle_annonce_processus, name="nouvelle_annonce_processus"),
	path('modifier_annonce/<int:ann_id>', views.modifier_annonce, name="modifier_annonce_page"),
	path('modifier_annonce_process/<int:ann_id>', views.modifier_annonce_process, name="modifier_annonce_process"),
	path('profile/', views.profile_page, name="profile_page"),
	path('generale_processus/', views.generale_processus, name="generale_processus"),
	path('adresse_processus/', views.adresse_processus, name="adresse_processus"),
	path('email_processus/', views.email_processus, name="email_processus"),
	path('password_processus/', views.password_processus, name="password_processus"),
	path('acheter/<str:categorie>', views.acheter, name="acheter_page"),
	path('acheter/', views.acheter, name="acheter_page"),
	path('produit/affecte_achat/<int:prod_id>', views.affecte_achat, name="affecte_achat"),
	path('produit/<prod_id>', views.produit, name="produit_page"),
	path('produit/go_payment/<int:prod_id>', views.go_payment, name="go_payment"),
	path('supprimer_produit/<int:prod_id>', views.supprimer_produit, name="supprimer_produit_process"),
	path('supprimer_compte/<int:user_id>', views.supprimer_compte, name="supprimer_compte_process"),
	#path('acheter_by_categorie/<str:categorie>', views.acheter_by_categorie, name="acheter_by_categorie_process")
]