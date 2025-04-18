from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django import views
from Admins import views

urlpatterns=[
path('administrateur/gerer-produits.html',views.GererProduits,name="gererProduits"),
path('administrateur/gerer-demandes.html',views.GererDemandes,name="gererDemandes"),
path('administrateur/liste-demande-validée.html',views.ListeDemandesV,name="listeDemandesV"),
path('administrateur/gerer-clients.html',views.GererClients,name="gererClients"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)