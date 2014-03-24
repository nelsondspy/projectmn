from django.db import models

 
from projectman.apps.admin.models import Fase


""" Modelo ItemTipos : agrupan tipos de atributos 
-un tipo de item depende de la existencia de una fase
"""
class ItemTipos(models.Model):
    idtipoitem = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40 , blank=False , help_text='Nombre')
    descripcion = models.CharField(max_length=80, null=True, blank=True ,help_text='Descripcion')
    #claves foraneas    
    idfase = models.ForeignKey(Fase)
    
    def __unicode__(self):
        return self.nombre


"""Modelo Item  """
class Item(models.Model):
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

""" tipos de atributos
-un tipo de atributo depende de un tipo de item
"""
class AtributoTipos(models.Model):
    TIPOS_DATOS = (
        ('C', 'caracter'),
        ('N', 'numerico'),
        ('D', 'fecha'),
    )
    idtipoatributo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=80)
    tipodato = models.CharField(max_length=1, choices=TIPOS_DATOS)
    #relaciones 
    idtipoitem = models.ForeignKey(ItemTipos)


"""Modelo AtributoIntancias: instancias de los tipos de atributos, 
-una instancia de atributo depende de la existencia del item
-una instancia de atributo depende de la existencia del tipo de atributo 
"""
class AtributoIntancias(models.Model):
    idinstancia =  models.AutoField(primary_key=True)
    valor = models.CharField(max_length=50) 
    usoactual = models.BooleanField()
    fcreacion = models.DateField(auto_now=True)
    #relaciones 
    iditem = models.ForeignKey(Item)
    idtipoatributo = models.ForeignKey(AtributoTipos)


