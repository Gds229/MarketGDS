from datetime import datetime
import os
from django.shortcuts import render
from django.conf import settings

from Clients.models import Clients, Demandes, Produits

# Create your views here.
def GererProduits(request):
    messages=""
    produits=Produits.objects.all().order_by('-id')
    if request.method=='POST':
        nom=request.POST.get('nom')
        prix=request.POST.get('prix')
        image=request.FILES.get('image')
        descrip=request.POST.get('descrip')
        r=Produits(
            nom=nom,
            prix=prix,
            descrip=descrip,
            date_ajoute=datetime.today().now(),
            image=image
        )
        r.save()
        if r:
         #Enregistrer les images
         imagee=request.FILES['image']
         destination =  os.path.join(settings.MEDIA_ROOT, 'produits')
         file_path = os.path.join(destination, imagee.name)
         with open(file_path, 'wb') as destination:
            for chunk in imagee.chunks():
             destination.write(chunk)
            if chunk:
             return render(request,'administrateur/gerer-produits.html',{'messages':messages,'produits':produits})
        else:
            message="Echec" 
            return render(request,'administrateur/gerer-produits.html',{'messages':messages,'produits':produits}) 
    return render(request,'administrateur/gerer-produits.html',{'messages':messages,'produits':produits})


def GererDemandes(request):
    messages=""
    demandes=Demandes.objects.all().order_by('-id')
    return render(request,'administrateur/gerer-demandes.html',{'messages':messages,'demandes':demandes})

def ListeDemandesV(request):
    messages=""
    demandesV=Demandes.objects.filter().order_by('-id')
    return render(request,'administrateur/liste-demande-validée.html',{'messages':messages,'demandesV':demandesV})
def GererClients (request):
    messages=""
    clients=Clients.objects.all()
    return render(request,'administrateur/gerer-clients.html',{'messages':messages,'clients':clients})

