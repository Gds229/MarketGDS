from django.db import models

# Create your models here.
class Clients(models.Model):
    nom=models.CharField(max_length=100,default='')
    prénom=models.CharField(max_length=100,default='')
    username=models.CharField(max_length=100,default='')
    password=models.CharField(max_length=100,default='')
    mail=models.CharField(max_length=100,default='')
    tel=models.CharField(max_length=100)
    sexe=models.CharField(max_length=100,default='')
    statut=models.CharField(max_length=100,default='utilisateur')
    image=models.ImageField(upload_to='images/', blank=True, null=True)# Spécifiez le dossier de téléchargement des images
    
    def __init__(self, *args, **kwargs):
        images = kwargs.pop('image', None)
        super().__init__(*args, **kwargs)
        if images:
            self.image = images
    
class Produits(models.Model):
    nom=models.CharField(max_length=100,default='')
    prix=models.IntegerField()
    descrip=models.CharField(max_length=300,default='')
    date_ajoute=models.DateField()
    image=models.ImageField(upload_to='images/', blank=True, null=True)# Spécifiez le dossier de téléchargement des images
    
    def __init__(self, *args, **kwargs):
        images = kwargs.pop('image', None)
        super().__init__(*args, **kwargs)
        if images:
            self.image = images
    
class Demandes(models.Model):
    qte=models.IntegerField()
    position=models.CharField(max_length=300,default='')
    date_enreg=models.DateField()
    desicions=models.BooleanField(default=False)
    clients=models.ForeignKey(Clients, related_name='clients', on_delete=models.CASCADE)
    produits=models.ForeignKey(Produits, related_name='prduits', on_delete=models.CASCADE)
    
    def PrixT (this):
        return this.qte * this.produits.prix