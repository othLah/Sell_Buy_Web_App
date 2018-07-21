from django import forms
from . import models
from django.conf import settings

class Register_Form(forms.ModelForm):
	SEXE = {
		("mâle", "mâle"),
		("female", "female")
	}

	username = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "150",
						"placeholder": "nom d'utilisateur...",
						"autofocus": "True",
						"required": "True"
					}
				)
		)
	email = forms.CharField(
			widget=forms.EmailInput(
					attrs = {
						"type": "email",
						"size": "30",
						"maxlength": "120",
						"placeholder": "email...",
						"required": "True"
					}
				)
		)
	password1 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"placeholder": "mot de passe...",
						"required": "True"
					}
				)
		)
	password2 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"placeholder": "confirmer mot de passe...",
						"required": "True"
					}
				)
		)
	sexe = forms.CharField(
			widget=forms.RadioSelect(
					choices=SEXE,
					attrs={
						"type": "radio",
						"name": "sexe",
						"required": "True"
					}
				)
		)
	nom = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"placeholder": "nom...",
						"required": "True"
					}
				)
		)
	prenom = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"placeholder": "prenom...",
						"required": "True"
					}
				)
		)
	rue_immeuble = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"placeholder": "rue/immeuble...",
						"required": "True"
					}
				)
		)
	numero = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"size": "30",
						"min": "1",
						"step": "1",
						"placeholder": "numéro...",
						"required": "True"
					}
				)
		)
	ville = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"placeholder": "ville...",
						"required": "True"
					}
				)
		)
	code_postal = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"min": "1",
						"step": "1",
						"placeholder": "code postal...",
						"required": "True"
					}
				)
		)
	tele = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "tele",
						"size": "30",
						"maxlength": "50",
						"placeholder": "téléphone: 06/05xxxxxxxx",
						"required": "True"
					}
				)
		)

	class Meta:
		model = models.Utilisateur
		fields = ["pays"]
		widgets = {
			"pays": forms.Select(
					attrs = {
						"maxlength": "120",
						"required": "True"
					}
				)
		}

class Login_Form(forms.Form):
	email_username = forms.CharField(
		widget=forms.TextInput(
				attrs = {
					"type": "text",
					"size": "30",
					"name": "text",
					"id": "id_email",
					"placeholder": "email, nom d'utilisateur...",
					"autofocus": "True",
					"required": "True"
				}
			)
		)
	password = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"name": "password",
						"id": "id_password",
						"size": "30",
						"maxlength": "120",
						"placeholder": "mot de passe...",
						"required": "True"
					}
				)
		)

class Nouvelle_Annonce_Form(forms.ModelForm):
	titre = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "50",
						"autofocus": "True",
						"required": "True"
					}
				)
		)
	prix = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"min": "0",
						"step": "1",
						"required": "True"
					}
				)
		)
	description = forms.CharField(
			widget=forms.Textarea(
					attrs = {
						"id": "txt",
						"rows": "10",
						"cols": "100",
						"maxLength": "1500",
						"placeholder": "1500 caractères au max...",
						"onkeyup" : "follow_textarea();",
						"required": "True"
					}
				)
		)
	photo1 = forms.ImageField(required=True,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in1",
						"onchange": "upload_pic(1);"
					}
				)
		)
	photo2 = forms.ImageField(required=False,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in2",
						"value": "{0}/none_image.png".format(settings.MEDIA_ROOT),
						"onchange": "upload_pic(2);"
					}
				)
		)
	photo3 = forms.ImageField(required=False,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in3",
						"onchange": "upload_pic(3);"
					}
				)
		)
	photo4 = forms.ImageField(required=False,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in4",
						"onchange": "upload_pic(4);"
					}
				)
		)
	photo5 = forms.ImageField(required=False,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in5",
						"onchange": "upload_pic(5);"
					}
				)
		)
	class Meta:
		model = models.Produit
		fields = ["categorie"]
		widgets = {
			"categorie": forms.Select(
					attrs = {
						"id": "select_cat",
						"required": "True"
					}
				)
		}
	del_p2 = forms.IntegerField(
			required=True,	max_value=1, min_value=0,
			widget=forms.NumberInput(
					attrs={
						"id": "del_p2"
					}
				)
		)
	del_p3 = forms.IntegerField(
			required=True,	max_value=1, min_value=0,
			widget=forms.NumberInput(
					attrs={
						"id": "del_p3"
					}
				)
		)
	del_p4 = forms.IntegerField(
			required=True,	max_value=1, min_value=0,
			widget=forms.NumberInput(
					attrs={
						"id": "del_p4"
					}
				)
		)
	del_p5 = forms.IntegerField(
			required=True,	max_value=1, min_value=0,
			widget=forms.NumberInput(
					attrs={
						"id": "del_p5"
					}
				)
		)

class Generale_Form(forms.Form):
	SEXE = {
		("mâle", "mâle"),
		("female", "female")
	}

	nom = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "20",
						"maxlength": "120",
						"required": "True"
					}
				)
		)
	prenom = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "20",
						"maxlength": "120",
						"required": "True"
					}
				)
		)
	username = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "20",
						"maxlength": "301",
						"placeholder": "format: Ancien/Nouveau",
						"required": "True"
					}
				)
		)
	tele = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "tele",
						"size": "20",
						"maxlength": "50",
						"required": "True"
					}
				)
		)
	sexe = forms.CharField(
			widget=forms.RadioSelect(
					choices=SEXE,
					attrs={
						"type": "radio",
						"name": "sexe",
						"required": "True"
					}
				)
		)

class Adresse_Form(forms.ModelForm):
	rue_immeuble = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"id": "rue_immeuble",
						"required": "True"
					}
				)
		)
	numero = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"size": "30",
						"min": "1",
						"step": "1",
						"id": "num",
						"required": "True"
					}
				)
		)
	ville = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						"type": "text",
						"size": "30",
						"maxlength": "120",
						"id": "ville",
						"required": "True"
					}
				)
		)
	code_postal = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"min": "1",
						"step": "1",
						"id": "code_pos",
						"required": "True"
					}
				)
		)

	class Meta:
		model = models.Utilisateur
		fields = ["pays"]
		widgets = {
			"pays": forms.Select(
					attrs = {
						"id": "pays",
						"maxlength": "120",
						"required": "True"
					}
				)
		}

class Email_Form(forms.Form):
	old_email = forms.CharField(
			widget=forms.EmailInput(
					attrs = {
						"type": "email",
						"size": "30",
						"maxlength": "120",
						"id": "old_email",
						"required": "True"
					}
				)
		)
	new_email = forms.CharField(
			widget=forms.EmailInput(
					attrs = {
						"type": "email",
						"size": "30",
						"maxlength": "120",
						"id": "new_email",
						"required": "True"
					}
				)
		)
	confirm_new_email = forms.CharField(
			widget=forms.EmailInput(
					attrs = {
						"type": "email",
						"size": "30",
						"maxlength": "120",
						"id": "r_new_email",
						"required": "True"
					}
				)
		)

class MotDePasse_Form(forms.Form):
	old_password = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"id": "old_pass",
						"required": "True"
					}
				)
		)
	new_password = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"id": "new_pass",
						"required": "True"
					}
				)
		)
	confirm_new_password = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"id": "old_pass",
						"required": "True"
					}
				)
		)

class Acheter_Form(forms.ModelForm):
	TRIER_PAR = {
		("date_depot", "Date: 1 - 30"),
		("-date_depot", "Date: 30 - 1"),
		("titre", "Alphabet: A - Z"),
		("-titre", "Alphabet: Z - A"),
		("prix", "Prix: $ - $$"),
		("-prix", "Prix: $$ - $")
	}

	trier_par = forms.CharField(
			widget=forms.Select(
					choices = TRIER_PAR,
					attrs = {
						"name": "trie_par",
						"id": "select_trie",
						"required": "True"
					}
				)
		)
	min_prix = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"name": "min_max",
						"id": "in1",
						"size": "6",
						"min": "0",
						"step": "1",
						"placeholder": "min..."
					}
				), required=False
		)
	max_prix = forms.IntegerField(
			widget=forms.NumberInput(
					attrs = {
						"type": "number",
						"name": "min_max",
						"id": "in2",
						"size": "6",
						"min": "0",
						"step": "1",
						"placeholder": "max...",
					}
				), required=False
		)
	class Meta:
		model = models.Produit
		fields = ["categorie"]
		widgets = {
			"categorie": forms.Select(
					attrs = {
						"id": "select_cat",
						"required": "False"
					}
				)
		}

class Modifier_Annonce(Nouvelle_Annonce_Form):
	photo1 = forms.ImageField(required=False,
			widget = forms.FileInput(
					attrs = {
						"type": "file",
						"id": "small_in1",
						"onchange": "upload_pic(1);"
					}
				)
		)

class Verify_Form(forms.Form):
	code_ch = forms.CharField(required=True,
			widget=forms.TextInput(
					attrs={
						"type": "text",
						"size": "30",
						"maxlength": "24",
						"placeholder": "code de vérification..."
					}
				)
		)

class Reset_Password_Email(forms.Form):
	email = forms.CharField(
			widget=forms.EmailInput(
					attrs = {
						"type": "email",
						"size": "30",
						"maxlength": "120",
						"placeholder": "email...",
						"required": "True"
					}
				)
		)

class Reset_Password_Password(forms.Form):
	password = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						"type": "password",
						"size": "30",
						"maxlength": "120",
						"placeholder": "mot de passe...",
						"required": "True"
					}
				)
		)

class Search_Bar(forms.Form):
	bar = forms.CharField(required=False,
			widget=forms.TextInput(
					attrs = {
						"type": "search",
						"size": "30",
						"placeholder": "recherche..."
					}
				)
		)