from genericpath import exists
import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
import codecs
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden

from Clients.models import Clients, Produits

# Create your views here.
def Home(request):
    return render(request,'index.html')

def Login(request):
    messages=''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username).first()
        if user:
                auth_user=authenticate(username=user.username,password=password) 
                if auth_user:
                    clt=Clients.objects.get(username=username,password=password)
                    if clt.statut == 'utilisateur': 
                        login(request,auth_user)
                        produits=Produits.objects.all().order_by('-id')
                        return render(request,'utilisateur/produits.html',{'messages':messages,'produits':produits})
                    if clt.statut == 'administrateur':
                        login(request,auth_user)
                        produits=Produits.objects.all().order_by('-id')
                        return render(request,'administrateur/gerer-produits.html',{'messages':messages,'produits':produits})
                else:
                    messages='Erreur d\'authentification'
                    return render(request,'login.html',{'messages':messages})  
        else:
            messages='L\'utilisateur n\' existe pas'
            return render(request,'login.html',{'messages':messages})             
    else:
        messages=''
        return render(request,'login.html',{'messages':messages})


def Register(request):
      message=""
      #postes=Postes.objects.all()
      if request.method=='POST':
         nom=request.POST.get('nom')
         prenom=request.POST.get('prenom')
         username=request.POST.get('username')
         mail=request.POST.get('mail')
         tel=request.POST.get('tel')
         image=request.FILES.get('image')
         sexe=request.POST.get('sexe')
         password=request.POST.get('password')
         Cpassword=request.POST.get('cpassword')
     
         #Vérifier si le tel et email existe déja
         if Clients.objects.filter(tel=tel).exists():
            messages = "Ce numéro de téléphone est déjà enregistré veillez saisir un autre."
            return render(request,  'register.html', {'messages':messages})
         else:
             if Clients.objects.filter(mail=mail).exists():
               messages = "Ce mail est déjà enregistré veillez saisir un autre."
               return render(request, 'register.html', {'messages':messages})
             else:
                if Clients.objects.filter(password=password).exists():
                  messages = "Ce mot de passe existe déjà"
                  return render(request, 'register.html', {'messages':messages})
                else:
                   if str(password)==str(Cpassword):
                    #""" Création d'une instance du personnel """
                    u=Clients(
                     nom=nom,
                     prénom=prenom,
                     username=username,
                     password=password,
                     mail=mail,
                     tel=tel,
                     sexe=sexe,
                     image=image,   
                     )
                    r=User(
                        username=username,
                        email=mail,
                     )
                    r.password=password
                    r.set_password(r.password)
                     #""" Enregistrement dans la base de donnée """
                    u.save(),
                    r.save(),
                    if u:
                     #Enregistrer les images
                     imagee=request.FILES['image']
                     destination =  os.path.join(settings.MEDIA_ROOT, 'images')
                     file_path = os.path.join(destination, imagee.name)
                     with open(file_path, 'wb') as destination:
                        for chunk in imagee.chunks():
                         destination.write(chunk)
                     if chunk:
                        return render(request,'login.html')
                    else:
                     message="Echec" 
                   else:
                    message = "le mot de passe et la confirmation ne sont identiques"
                    return render(request, 'register.html', {'messages':message})
      return render(request,'register.html',{'messages':message})

def ForgetPassword(request):
    messages=''
    try:
        if request.method=='POST':
            email=request.POST.get('mail')
            print(email)
            user=User.objects.filter(email=email).first()
            if user:
                token=default_token_generator.make_token(user)
                uid=urlsafe_base64_encode(force_bytes(user.id))
                current_site=request.META['HTTP_HOST']
                html_text=render_to_string("email.html",{"token":token,"uid":uid,"domaine":f"http://{current_site}"})
                send_mail(
                        'Mot de passe oublié',
                        'Gds-Shop',
                        'settings.EMAIL_HOST_USER', 
                        'aimegbadessi@gmail.com',
                        [email],
                        fail_silently=False,
                        html_message=html_text
                    )
                if send_mail:
                    messages='E-mail envoyé avec succès'
                else:
                    messages='Erreur lors de l\'envoi de l\'e-mail et n\'est pas envoyé'
            else:
                messages='Le mail n\'existe pas'
    except Exception as e:
            # Vous pouvez personnaliser le message d'erreur ou la gestion d'exception
            messages=f"Une erreur s'est produite : vérifier votre connexion et votre mail."
            return render(request,'forget-password.html',{'messages':messages})
    return render(request,'forget-password.html',{'messages':messages})

def ResetPassword(request):
    messages=""
    try:
       user_id=urlsafe_base64_decode(uid)
       decode_uid=codecs.decode(user_id,'utf-8')
       user=User.objects.get(id=decode_uid)
    except:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier ce mot de passe. Utilisateur introuvable.")
    check_token=default_token_generator.check_token(user,token)
    if not check_token:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier ce mot de passe. Votre token est invalid ou.")
    
    error=False
    success=False
    messages=""
    if request.method == 'POST':
        password=request.POST.get('password')
        Cpassword=request.POST.get('cpassword')
        print(password,Cpassword)
        if password==Cpassword:
            try:
                validate_password(password,user)
                user.set_password(password)
                user.save()
                messages="Votre mot de passe à été modifié avec succès"
            except ValidationError :
                messages="Votre mail est invalide"
        else:
            messages="les eux mot de passe ne sont pas identiques"
    return render(request,'reset-password.html',{'messages':messages})

def ResetPassword(request):
    return render(request,'reset-password.html')

def Produits(request):
    return render(request,'utilisateur/produits.html')

def VosDemandes(request):
    return render(request,'utilisateur/vos-demandes.html')

def DemandesRéçu(request):
    return render(request,'utilisateur/demandes-reçu.html')

def Base(request):
    return render(request,'utilisateur/base.html')

def CommandeProduits(request,idProduit):
    messages=""
    return render(request,'utilisateur/commande-produits.html',{'messages':messages})




