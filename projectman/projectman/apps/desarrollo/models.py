from django.db import models
from django.core.urlresolvers import reverse

 
from projectman.apps.admin.models import Fase


class ItemTipos(models.Model):
    """
    
    Modelo ItemTipos : agrupan tipos de atributos. 
    -un tipo de item depende de la existencia de una fase
    
    """

    idtipoitem = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40 , blank=False , help_text='Nombre', null=False)
    descripcion = models.CharField(max_length=80, null=True, blank=True ,help_text='Descripcion')
    #claves foraneas    
    idfase = models.ForeignKey(Fase)
    
    def __unicode__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('tipoitem_editar', kwargs={'pk': self.pk})


class ItemAtributos(models.Model):
    """ 
    
    ItemAtributos, un atributo tiene un nombre es un tipo de valor.
    -un tipo de atributo depende de un tipo de item
    
    """

    TIPOS_DATOS = (
        ('C', 'caracter'),
        ('N', 'numerico'),
        ('D', 'fecha'),
    )
    idatributo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    tipodato = models.CharField(max_length=1, choices=TIPOS_DATOS)
    #relaciones 
    idtipoitem = models.ForeignKey(ItemTipos)

    def __unicode__(self):
        return self.nombre



class Item(models.Model):
    """
    
    Modelo Item. un item es la unidad principal del modulo de desarrollo.
    Tiene un tipo de item , y por ende posee los atributos definidos del tipo
    
    """
    E_DESAPROBADO = 'DES'
    E_APROBADO = 'APR'
    E_REVISION = 'REV'
    E_BLOQUEADO = 'BLO'
    
    ESTADOS = (
               (E_DESAPROBADO, 'Desaprobado'),
               (E_APROBADO, 'Aprobado'),
               (E_REVISION, 'Revision'),
               (E_BLOQUEADO, 'Bloqueado'),
               )
    
    iditem = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    nombre = models.CharField(max_length=40, null=False)
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    estado = models.CharField(max_length=3)
    version = models.IntegerField()
    #relaciones 
    idfase = models.ForeignKey(Fase)
    idtipoitem = models.ForeignKey(ItemTipos)
    
    
    def sigte_numero(self):
        #ultimo = Item.objects.filter(idfase=self.idfase).order_by('numero')[0]
        ultimo = Item.objects.filter(idfase=self.idfase).count()
        if ultimo: 
            self.numero = ultimo + 1
        else:
            self.numero = 1



class ItemAtributosValores(models.Model):
    """
    
    Modelo que relaciona el item  y los atributos.
    Representa a una valor en particular de una atributo para un item  
    Su existencia depende tanto del item como del atributo 
    
    """

    idvalor =  models.AutoField(primary_key=True)
    valor = models.CharField(max_length=50) 
    usoactual = models.BooleanField()
    creacion = models.DateField(auto_now=True)
    
    #relaciones 
    iditem = models.ForeignKey(Item)
    idatributo = models.ForeignKey(ItemAtributos)


