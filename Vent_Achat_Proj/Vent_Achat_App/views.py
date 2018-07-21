from django.shortcuts import render, redirect
from . import forms, models
from django.views.decorators.http import require_POST
import re
from django.conf import settings
import random
from django.db.models import Max
from django.core.mail import send_mail
import smtplib
from django.urls import reverse

where_to_go = "accueil_page"
args_to_go = None

def check_length(maxi, *args):
	for arg in args:
		if len(str(arg))<0 or len(str(arg))>maxi:
			return False
	return True

def accueil(request):
	all_p = models.Produit.objects.all()
	if all_p.count() > 5:
		prods = []
		t = 1
		choice = None
		while len(prods) < 5:
			if t == 1:
				rand_from = all_p.filter(categorie__exact="Téléphone")
				if len(rand_from) != 0:
					choice = random.choice(rand_from)
			elif t == 2:
				rand_from = all_p.filter(categorie__exact="Tablette")
				if len(rand_from) != 0:
					choice = random.choice(rand_from)
			elif t == 3:
				rand_from = all_p.filter(categorie__exact="Ordinateur")
				if len(rand_from) != 0:
					choice = random.choice(rand_from)
			elif t == 4:
				rand_from = all_p.filter(categorie__exact="Appareil Photo")
				if len(rand_from) != 0:
					choice = random.choice(rand_from)
			else:
				rand_from = all_p.filter(categorie__exact="Autre")
				if len(rand_from) != 0:
					choice = random.choice(rand_from)

			if choice != None:
				if not choice in prods:
					prods.append(choice)
				t += 1
			elif t == 5:
				t = 1
			else:
				t += 1
	else:
		prods = all_p
	search = forms.Search_Bar()
	dico = {
		"recommended_prods": prods,
		"search_bar": search
	}
	return render(request, 'accueil.html', dico)

def enregistrer(request):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				return redirect("accueil_page")
			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")

	re_inputs = forms.Register_Form()
	re_inputs.fields["pays"].initial = "Morocco"
	dico = {"inputs": re_inputs}
	return render(request, 'register.html', dico)

def generer_code(max_t):
	code = ""
	while(len(code) < max_t):
		if max_t == 8:
			if random.randint(0, 1) == 1:
				code += chr(random.randint(97, 122))
			else:
				code += chr(random.randint(65, 90))

			if random.randint(0, 1) == 1:
				code += random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '.', '+', '-', '_'])
		else:
			code += chr(random.randint(33, 125))
	return code

def send_email(email, content):
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login("electro.sb1@gmail.com", "eSelleBuy1")

		server.sendmail("oth.lahrimi1996@gmail.com", email, content)
	except:
		return False

	server.quit()
	return True

@require_POST
def enregistrement(request):
	new_user = forms.Register_Form(request.POST)
	try:
		if new_user.is_valid():
			username = new_user.cleaned_data["username"]
			email = new_user.cleaned_data["email"].lower()
			password1 = new_user.cleaned_data["password1"]
			password2 = new_user.cleaned_data["password2"]
			sexe = new_user.cleaned_data["sexe"]
			nom = new_user.cleaned_data["nom"]
			prenom = new_user.cleaned_data["prenom"]
			rue_immeuble = new_user.cleaned_data["rue_immeuble"]
			numero = new_user.cleaned_data["numero"]
			ville = new_user.cleaned_data["ville"]
			code_postal = new_user.cleaned_data["code_postal"]
			pays = new_user.cleaned_data["pays"]
			tele = new_user.cleaned_data["tele"]
			username_exp = r"[0-9a-zA-Z@\.+\-_]+"
			if not models.Utilisateur.objects.filter(username__exact=username).exists() and 0<len(username)<=150:
				if re.match(username_exp, username):
					if not models.Utilisateur.objects.filter(email__iexact=email).exists() and 0<len(email)<=120:
						if password1 == password2:
							if 8<=len(password1)<=120:
								if not models.Utilisateur.objects.filter(password__exact=password1).exists():
									if check_length(120, nom, prenom, rue_immeuble, ville) and check_length(10, tele) and tele.isdigit() and numero>0 and code_postal>0:
										code = generer_code(24)
										if send_email(email, code):
											user = models.Utilisateur.objects.create(
													username=username,
													email=email,
													password=password1,
													sexe=sexe,
													nom=nom,
													prenom=prenom,
													rue_immeuble=rue_immeuble,
													numero=numero,
													ville=ville,
													code_postal=code_postal,
													pays=pays,
													tele=tele,
													verification_code=code
												)
											request.session["userID"] = user.id
											return redirect("verifier_page")
										else:
											assert 1 == 2
									else:
										assert 1 == 2
								else:
									assert 1 == 2
							else:
								assert 1 == 2
						else:
							assert 1 == 2
					else:
						assert 1 == 2
				else:
					assert 1 == 2
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=

			=> "nom d'utilisateur" doit être unique.
			
			=> "nom d'utilisateur" doit contenir 150 caractères au maximum.
			
			=> "nom d'utilisateur" doit contenir des lettres, des chiffres, @, ., -, +, _.
			
			=> "email" doit être unique.
			
			=> "email" doit contenir 120 caractères au maximum.
			
			=> "mot de passe" et "répéter mot de passe" doivent être uniques.
			
			=> "mot de passe" et "répéter mot de passe" doivent être les mêmes.
			
			=> "mot de passe" et "répéter mot de passe" doivent contenir entre 8 et 120 caractères.
			
			=> "numéro" et "code" doivent être supérieur à 0.
			
			=> Vous devez s'enregistrer avec une connexion active.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

def verifier(request):
	if "userID" in request.session and not models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
		verify_in = forms.Verify_Form()
		dico = {
			"inputs": verify_in
		}
		return render(request, "verify_page.html", dico)
	return redirect("accueil_page")

@require_POST
def verifier_process(request):
	if "userID" in request.session and not models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
		code_form = forms.Verify_Form(request.POST)
		if code_form.is_valid():
			user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
			if user.verification_code == code_form.cleaned_data["code_ch"]:
				user.verified = True
				user.save()
				return redirect("connexion_page")

		return redirect("verifier_page")

	return redirect("accueil_page")

def reenvoyer_code(request):
	if "userID" in request.session:
		try:
			user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
			if not user.verified:
				code = generer_code(24)
				user.verification_code = code
				user.save()
				if send_email(user.email, user.verification_code):
					return redirect("verifier_page")
				assert 1 == 2
			return redirect("accueil_page")
		except:
			return redirect("deconnexion_processus")
	return redirect("connexion_page")


def connexion(request):
	try:
		if "userID" in request.session:
			return redirect("accueil_page")
	except:
		return redirect("deconnexion_processus")

	co_inputs = forms.Login_Form()
	dico = {"inputs": co_inputs}
	return render(request, 'login.html', dico)

@require_POST
def connexion_p(request):
	user = forms.Login_Form(request.POST)
	try:
		if user.is_valid():
			email = user.cleaned_data["email_username"].lower()
			username = user.cleaned_data["email_username"]
			recognize = None
			if models.Utilisateur.objects.filter(email__exact=email).exists():
				recognize = models.Utilisateur.objects.get(email__exact=email)
			elif models.Utilisateur.objects.filter(username__exact=username).exists():
				recognize = models.Utilisateur.objects.get(username__exact=username)
			else:
				assert 1 == 2

			if recognize.password == user.cleaned_data["password"]:
				request.session["userID"] = recognize.id
				print("\n\n{0}\n\n".format(where_to_go))
				return redirect(reverse(where_to_go, args=args_to_go))
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=

			=> "email/nom d'utilisateur" ou "mot de passe" ne sont pas correcte.
			
			=> Inéxistant "email/nom d'utilisateur".
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

def mdp_email(request):
	if "userID" in request.session:
		return redirect("accueil_page")

	email_in = forms.Reset_Password_Email()
	dico = {
		"inputs": email_in
	}
	return render(request, "reset_pass_email.html", dico)

@require_POST
def mdp_pass(request):
	if "userID" in request.session:
		return redirect("accueil_page")

	email_f = forms.Reset_Password_Email(request.POST)
	if email_f.is_valid():
		try:
			user = models.Utilisateur.objects.get(email__iexact=email_f.cleaned_data["email"])
			passw = generer_code(8)
			user.password = passw
			if send_email(user.email, passw):
				user.save()

				mdp_f = forms.Reset_Password_Password()
				dico = {
					"inputs": mdp_f,
					"user": user.id
				}
				return render(request, "reset_pass_pass.html", dico)
		except:
			return redirect("vendre_page")
		
	return redirect("mdp_email_page")

@require_POST
def mdp_verifier(request, user_id):
	if "userID" in request.session:
		return redirect("accueil_page")

	pass_f = forms.Reset_Password_Password(request.POST)
	if pass_f.is_valid():
		try:
			user = models.Utilisateur.objects.get(id__exact=user_id)
			if user.password == pass_f.cleaned_data["password"]:
				request.session["userID"] = user.id
				return redirect("accueil_page")
		except:
			return redirect("connexion_page")

	return redirect("mdp_pass_page")

def vendre(request):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				infos = models.Produit.objects.filter(user_id__exact=request.session["userID"])
				search = forms.Search_Bar()
				dico = {
					"infos": infos,
					"search_bar": search
				}
				return render(request, 'vendre.html', dico)
			
			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")

	global where_to_go
	where_to_go = "vendre_page"
	print("\n\n{0}\n\n".format(where_to_go))
	return redirect('connexion_page')

def deconnexion(request):
	global where_to_go
	where_to_go = "accueil_page"

	global args_to_go
	args_to_go = None

	if "userID" in request.session:
		del request.session["userID"]
		return redirect("accueil_page")

	return redirect("accueil_page")

def nouvelle_annonce(request):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				n_a_inputs = forms.Nouvelle_Annonce_Form()
				search = forms.Search_Bar()
				dico = {
					"inputs": n_a_inputs,
					"search_bar": search
				}
				return render(request, "nouvelle_annonce.html", dico)

			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")

	global where_to_go
	where_to_go = "nouvelle_annonce_page"
	return redirect("connexion_page")

@require_POST
def nouvelle_annonce_processus(request):
	#try:
	if "userID" in request.session:
		new_annonce = forms.Nouvelle_Annonce_Form(request.POST, request.FILES)
		if new_annonce.is_valid():
			if check_length(120, new_annonce.cleaned_data["titre"]) and check_length(14, new_annonce.cleaned_data["prix"]) and check_length(1500, new_annonce.cleaned_data["description"]) and check_length(14, new_annonce.cleaned_data["categorie"]):
				product = models.Produit.objects.create(
						titre = new_annonce.cleaned_data["titre"],
						categorie = new_annonce.cleaned_data["categorie"],
						prix = new_annonce.cleaned_data["prix"],
						photo1 = new_annonce.cleaned_data["photo1"],
						description = new_annonce.cleaned_data["description"],
						user_id=models.Utilisateur.objects.get(id__exact=request.session["userID"])
					)
				for i in [2, 3, 4, 5]:
					if new_annonce.cleaned_data["photo{0}".format(i)]!=None and new_annonce.cleaned_data["del_p{0}".format(i)]==0:
						if i == 2:
							product.photo2 = new_annonce.cleaned_data["photo2"]
						elif i == 3:
							product.photo3 = new_annonce.cleaned_data["photo3"]
						elif i == 4:
							product.photo4 = new_annonce.cleaned_data["photo4"]
						else:
							product.photo5 = new_annonce.cleaned_data["photo5"]
				product.save()
				return redirect("vendre_page")
				'''else:
					assert 1 == 2
			else:
				assert 1 == 2
		else:
			return redirect("connexion_page")
	except:
		infos = """  => ERROR <=

			=> "titre" ou "prix" ou "categorie" ou "description" ne sont pas valides.
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)'''

	return redirect("accueil_page")

def modifier_annonce(request, ann_id):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				try:
					ann = models.Produit.objects.get(id__exact=ann_id)
					if ann.user_id.id == request.session["userID"]:
						ann_form = forms.Modifier_Annonce()
						ann_form.fields["titre"].initial = ann.titre
						ann_form.fields["categorie"].initial = ann.categorie
						ann_form.fields["prix"].initial = ann.prix
						ann_form.fields["description"].initial = ann.description

						search = forms.Search_Bar()
						dico = {
							"f_inputs": ann_form,
							"ann_fields": ann,
							"search_bar": search
						}
						return render(request, "modifier_annonce.html", dico)
					
					return redirect('vendre_page')
				except:
					return redirect('vendre_page')

			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")
	
	global where_to_go
	where_to_go = "modifier_annonce_page"
	global args_to_go
	args_to_go = [ann_id]

	return redirect('connexion_page')

@require_POST
def modifier_annonce_process(request, ann_id=0):
	if "userID" in request.session:
		try:
			prod = models.Produit.objects.get(id__exact=ann_id)
			if prod.user_id.id == request.session["userID"]:
				modif_form = forms.Modifier_Annonce(request.POST, request.FILES)
				if modif_form.is_valid():
					prod.titre = modif_form.cleaned_data["titre"]
					prod.categorie = modif_form.cleaned_data["categorie"]
					prod.prix = modif_form.cleaned_data["prix"]
					prod.description = modif_form.cleaned_data["description"]

					print("\n")
					for i in [1, 2, 3, 4, 5]:
						print("{0}".format(modif_form.cleaned_data["photo{0}".format(i)]))
					print("\n")

					if modif_form.cleaned_data["photo1"] != None:
						prod.photo1 = modif_form.cleaned_data["photo1"]

					for i in [2, 3, 4, 5]:
						if modif_form.cleaned_data["del_p{0}".format(i)] == 1:
							if i == 2:
								prod.photo2 = settings.MEDIA_ROOT + "/none_image.png"
							elif i == 3:
								prod.photo3 = settings.MEDIA_ROOT + "/none_image.png"
							elif i == 4:
								prod.photo4 = settings.MEDIA_ROOT + "/none_image.png"
							else:
								prod.photo5 = settings.MEDIA_ROOT + "/none_image.png"
						else:
							if modif_form.cleaned_data["photo{0}".format(i)] != None:
								if i == 2:
									prod.photo2 = modif_form.cleaned_data["photo2"]
								elif i == 3:
									prod.photo3 = modif_form.cleaned_data["photo3"]
								elif i == 4:
									prod.photo4 = modif_form.cleaned_data["photo4"]
								else:
									prod.photo5 = modif_form.cleaned_data["photo5"]

					prod.save()
					return redirect("vendre_page")
				else:
					return redirect("accueil_page")
			else:
				return redirect("vendre_page")
		except:
			return redirect("vendre_page")
	else:
		return redirect("connexion_page")

	return redirect("vendre_page")


def profile_page(request):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				user = models.Utilisateur.objects.get(id__exact=request.session["userID"])

				g_form = forms.Generale_Form()
				g_form.fields["nom"].initial = user.nom
				g_form.fields["prenom"].initial = user.prenom
				g_form.fields["tele"].initial = user.tele
				g_form.fields["sexe"].initial = user.sexe

				a_form = forms.Adresse_Form()
				a_form.fields["rue_immeuble"].initial = user.rue_immeuble
				a_form.fields["numero"].initial = user.numero
				a_form.fields["ville"].initial = user.ville
				a_form.fields["code_postal"].initial = user.code_postal
				a_form.fields["pays"].initial = user.pays

				e_form = forms.Email_Form()
				p_form = forms.MotDePasse_Form()

				search = forms.Search_Bar()

				dico = {
					"generale_in": g_form,
					"adresse_in": a_form,
					"email_in": e_form,
					"motdepasse_in": p_form,
					"user_id_nbre": request.session["userID"],
					"search_bar": search
					}
				return render(request, 'profile.html', dico)

			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")

	global where_to_go
	where_to_go = "profile_page"
	return redirect("connexion_page")

@require_POST
def generale_processus(request):
	new_infos = forms.Generale_Form(request.POST)
	try:
		if new_infos.is_valid():
			nom = new_infos.cleaned_data["nom"]
			prenom = new_infos.cleaned_data["prenom"]
			usernames = new_infos.cleaned_data["username"].split("/")
			tele = new_infos.cleaned_data["tele"]
			sexe = new_infos.cleaned_data["sexe"]
			if len(usernames) == 2:
				user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
				if usernames[0] == user.username:
					username_exp = r"[0-9a-zA-Z@\.+\-_]+"
					if re.match(username_exp, usernames[1]):
						if check_length(120, nom, prenom) and check_length(50, tele) and check_length(150, usernames[1]):
							user.nom = nom
							user.prenom = prenom
							user.username = usernames[1]
							user.tele = tele
							user.sexe = sexe
							user.save()
							return redirect("profile_page")
						else:
							assert 1 == 2
					else:
						assert 1 == 2
				else:
					assert 1 == 2
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=
			
			=> Invalide "nom d'utilisateur".
			
			=> "nouveau" nom d'utilisateur doit contenir 150 caractères au maximum.
			
			=> "nouveau" nom d'utilisateur doit contenir que des lettres, des chiffre, @, ., +, -, _.
			
			=> "nom" et "prénom" doivent contenir 120 caractères au maximum.
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

@require_POST
def adresse_processus(request):
	new_infos = forms.Adresse_Form(request.POST)
	try:
		if new_infos.is_valid():
			rue_immeuble = new_infos.cleaned_data["rue_immeuble"]
			numero = new_infos.cleaned_data["numero"]
			ville = new_infos.cleaned_data["ville"]
			code_postal = new_infos.cleaned_data["code_postal"]
			pays = new_infos.cleaned_data["pays"]
			if check_length(120, rue_immeuble, ville, pays) and numero>0 and code_postal>0:
				user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
				user.rue_immeuble =rue_immeuble
				user.numero = numero
				user.ville = ville
				user.code_postal = code_postal
				user.pays = pays
				user.save()
				return redirect("profile_page")
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=
			
			=> "rue_immeuble" et "ville" et "pays" doivent contenir 120 caractères au maximum.
			
			=> "numero" et "code_postal" doivent être supérieur à 0.
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

@require_POST
def email_processus(request):
	new_infos = forms.Email_Form(request.POST)
	try:
		if new_infos.is_valid():
			old_email = new_infos.cleaned_data["old_email"]
			new_email = new_infos.cleaned_data["new_email"]
			confirm_new_email = new_infos.cleaned_data["confirm_new_email"]
			if check_length(120, old_email, new_email, confirm_new_email):
				user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
				if old_email==user.email and new_email==confirm_new_email:
					user.email = new_email
					user.verified = False
					user.save()
					return redirect("verifier_page")
				else:
					assert 1 == 2
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=
			
			=> "ancien email" n'est pas correcte.
			
			=> "nouveau email" et "confirmer nouveau email" doivent être unique.
			
			=> "nouveau email" et "confirmer nouveau email" doivent être les mêmes.
			
			=> "nouveau email" et "confirmer nouveau email" doivent contenir 120 caractères au maximum.
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

@require_POST
def password_processus(request):
	new_infos = forms.MotDePasse_Form(request.POST)
	try:
		if new_infos.is_valid():
			old_pass = new_infos.cleaned_data["old_password"]
			new_pass = new_infos.cleaned_data["new_password"]
			confirm_new_pass = new_infos.cleaned_data["confirm_new_password"]
			if 8<=len(old_pass)<=120 and 8<=len(new_pass)<=120 and 8<=len(confirm_new_pass)<=120:
				user = models.Utilisateur.objects.get(id__exact=request.session["userID"])
				if old_pass==user.password and new_pass==confirm_new_pass:
					user.password = new_pass
					user.save()
					return redirect("profile_page")
				else:
					assert 1 == 2
			else:
				assert 1 == 2
		else:
			assert 1 == 2
	except:
		infos = """  => ERROR <=
			
			=> "ancien mot de passe" n'est pas correcte.
			
			=> "nouveau mot de passe" et "confirmer mot de passe" doivent être unique.
			
			=> "nouveau mot de passe" et "confirmer nouveau mot de passe" doivent être les mêmes.
			
			=> "nouveau mot de passe" et "confirmer nouveau mot de passe" doivent contenir entre 8 et 120 caractères.
			
			=> Hors Connexion.
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)

def acheter(request, categorie=None):
	prods = None
	if "categorie" in request.GET:
		infos = forms.Acheter_Form(request.GET)
		if infos.is_valid():
			categorie = infos.cleaned_data["categorie"]
			trier_par = infos.cleaned_data["trier_par"]
			min_prix = infos.cleaned_data["min_prix"]
			max_prix = infos.cleaned_data["max_prix"]
			prods = models.Produit.objects.all().order_by("{0}".format(trier_par))
			if categorie != None:
				prods = prods.filter(categorie__exact=categorie)
			if min_prix==None and max_prix!=None:
				prods = prods.filter(prix__lte=max_prix)
			elif min_prix!=None and max_prix==None:
				prods = prods.filter(prix__gte=min_prix)
			elif min_prix!=None and max_prix!=None:
				prods = prods.filter(prix__gte=min_prix).filter(prix__lte=max_prix)
	elif "bar" in request.GET:
		infos = forms.Search_Bar(request.GET)
		if infos.is_valid():
			to_s = infos.cleaned_data["bar"]
			if len(to_s) == 0:
				prods = models.Produit.objects.all().order_by("-date_depot")
			else:
				not_touch = r"[0-9a-zA-Zçüéâàêèïîû ]"
				for i in range(0, len(to_s)):
					if re.search(not_touch, to_s[i]) == None:
						to_s = to_s.replace(to_s[i], ' ')
				to_s = to_s.split()
				prods = []
				all_prods = models.Produit.objects.all()
				for p in all_prods:
					for s in to_s:
						if p.titre.lower().find(s.lower()) != -1:
							prods.append(p)
							break


	elif categorie!=None and categorie in ["Téléphone", "Tablette", "Ordinateur", "Appareil Photo", "Télévision", "Autre"]:
		prods = models.Produit.objects.filter(categorie__exact=categorie).order_by("-date_depot")
	else:
		prods = models.Produit.objects.all().order_by("-date_depot")

	ach_form = forms.Acheter_Form()
	search = forms.Search_Bar()
	dico = {
		"infos": prods,
		"inputs": ach_form,
		"user_loged": False,
		"search_bar": search
	}
	if len(prods) == 0:
		dico["nothing"] = True
	else:
		dico["nothing"] = False
	if "userID" in request.session:
		dico["user_loged"] = True
	return render(request, "acheter.html", dico)

def produit(request, prod_id=0):
	if prod_id != 0:
		try:
			prod = models.Produit.objects.get(id__exact=prod_id)
		except:
			return redirect("acheter_page")
		search = forms.Search_Bar()
		dico = {
			"infos": prod,
			"user_loged": False,
			"search_bar": search
		}
		if "userID" in request.session:
			dico["user_loged"] = True
		return render(request, "produit.html", dico)
	return redirect("acheter_page")

def supprimer_produit(request, prod_id=0):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				if prod_id > 0:
					try:
						prod = models.Produit.objects.get(id__exact=prod_id)
						if prod.user_id.id == request.session["userID"]:
							prod.delete()
							return redirect('vendre_page')
						
						infos = """  => ERROR <=

							=> Invalid Utilisateur.

							=> Hors Connexion.
						"""
						dico = {"info_key": infos}
						return render(request, "error.html", dico)
					except:
						infos = """  => ERROR <=

							=> Invalid Utilisateur.

							=> Hors Connexion.
						"""
						dico = {"info_key": infos}
						return render(request, "error.html", dico)

			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")

		infos = """  => ERROR <=

			=> Invalid Utilisateur.

			=> Hors Connexion
		"""
		dico = {"info_key": infos}
		return render(request, "error.html", dico)
	
	return redirect("connexion_page")

def netoyer_produits():
	for p in models.Produit.objects.filter(user_id__exact=None):
		p.delete()

def affecte_achat(request, prod_id=0):
	if "userID" in request.session:
		try:
			models.Produit.objects.get(id__exact=prod_id)
			dico = {"prod_id": prod_id}
			return render(request, "affecte_achat_process.html", dico)
		except:
			return redirect('acheter_page')
	
	global where_to_go
	where_to_go = "affecte_achat"
	global args_to_go
	args_to_go = [prod_id]
	
	return redirect("connexion_page")

def supprimer_compte(request, user_id=0):
	if "userID" in request.session:
		try:
			if models.Utilisateur.objects.get(id__exact=request.session["userID"]).verified:
				if user_id > 0:
					if request.session["userID"] == user_id:
						try:
							user = models.Utilisateur.objects.get(id__exact=user_id)
							user.delete()
							netoyer_produits();
							return redirect("deconnexion_processus")
						except:
							infos = """  => ERROR <=

								=> Invalid Utilisateur.

								=> Hors Connexion.
							"""
							dico = {"info_key": infos}
							return render(request, "error.html", dico)
					
					infos = """  => ERROR <=

						=>  Invalid Utilisateur.

						=> Hors Connexion.
					"""
					dico = {"info_key": infos}
					return render(request, "error.html", dico)

				infos = """  => ERROR <=

					=> Invalid Utilisateur.

					=> Hors Connexion.
				"""
				dico = {"info_key": infos}
				return render(request, "error.html", dico)

			return redirect("verifier_page")
		except:
			return redirect("deconnexion_processus")
	return redirect("connexion_page")

def go_payment(request, prod_id=0):
	if prod_id == 0:
		return redirect('acheter_page')
	elif not "userID" in request.session:
		return redirect('connexion_page')
	else:
		return render(reverse('paypal/process/', args=[prod_id]))
