from django.contrib import admin
from . import models

admin.site.register([models.Utilisateur, models.Produit, models.Acheter])