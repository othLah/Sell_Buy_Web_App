from django.db import models
from django.conf import settings

class Utilisateur(models.Model):
	TOUT_PAYS = {
		("Morocco", "Morocco")
	}
	SEXE = {
		("mâle", "mâle"),
		("female", "female")
	}

	username = models.CharField(max_length=150)
	email = models.EmailField()
	password = models.CharField(max_length=120)
	sexe = models.CharField(choices=SEXE, max_length=6)
	nom = models.CharField(max_length=120)
	prenom = models.CharField(max_length=120)
	rue_immeuble = models.CharField(max_length=120)
	numero = models.IntegerField()
	ville = models.CharField(max_length=120)
	code_postal = models.IntegerField()
	pays = models.CharField(choices=TOUT_PAYS, max_length=120)
	tele = models.CharField(max_length=120)
	date_creation = models.DateTimeField(auto_now_add=True)
	verified = models.BooleanField(default=False)
	verification_code = models.CharField(max_length=24, default="XXXXXXXXXXXXXXXXXXXXXXXX")

	def __str__(self):
		return 'Utilisateur N°{0}'.format(self.id)

class Produit(models.Model):
	CATEGORIES = {
		("Téléphone", "Téléphone"),
		("Tablette", "Tablette"),
		("Ordinateur", "Ordinataur"),
		("Appareil Photo", "Appareil Photo"),
		("Télévision", "Télévision"),
		("Autre", "Autre")
	}
	titre = models.CharField(max_length=50)
	categorie = models.CharField(choices=CATEGORIES, max_length=14)
	prix = models.IntegerField()
	photo1 = models.ImageField(default='{0}/none_image.png'.format(settings.MEDIA_ROOT))
	photo2 = models.ImageField(default='{0}/none_image.png'.format(settings.MEDIA_ROOT))
	photo3 = models.ImageField(default='{0}/none_image.png'.format(settings.MEDIA_ROOT))
	photo4 = models.ImageField(default='{0}/none_image.png'.format(settings.MEDIA_ROOT))
	photo5 = models.ImageField(default='{0}/none_image.png'.format(settings.MEDIA_ROOT))
	description = models.TextField()

	user_id = models.ForeignKey(Utilisateur, null=True, on_delete=models.SET_NULL)
	date_depot = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Produit N°{0}'.format(self.id)

class Acheter(models.Model):
	user_id = models.ForeignKey(Utilisateur, null=True, on_delete=models.SET_NULL)
	prod_id = models.ForeignKey(Produit, null=True, on_delete=models.SET_NULL)
	date_achat = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Achat N°{0}'.format(self.id)