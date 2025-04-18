from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django import views
from Clients import views

urlpatterns=[
path('',views.Home,name="home"),
path('login.html',views.Login,name="login"),
path('register.html',views.Register,name="register"),
path('forget-password.html',views.ForgetPassword,name="forgetPassword"),
path('reset-password.html',views.ResetPassword,name="resetPassword"),
path('utilisateur/produits.html',views.Produits,name="produits"),
path('utilisateur/vos-demandes.html',views.VosDemandes,name="vosDemandes"),
path('utilisateur/base.html',views.Base,name="base"),

path('utilisateur/demandes-réçu.html',views.DemandesRéçu,name="demandesReçu"),
path('utilisateur/commande-produits.html',views.CommandeProduits,name="commandeProduits")


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
