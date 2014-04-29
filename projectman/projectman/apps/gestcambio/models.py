from django.db import models
from ..admin.models import Proyecto
from  ..admin.models import Fase
from  ..desarrollo.models import Item
from django.contrib.auth.models import User

class ComiteProyecto(models.Model):
    """
    
    Un comite esta conformado por el par: proyecto , usuario.
    
    """
    id = models.AutoField(primary_key=True)
    #claves foraneas
    proyecto = models.ForeignKey(Proyecto)
    usuario = models.ForeignKey(User)
    

#LineaBase
class LineaBase(models.Model):
    """
    
    Modelo cabecera de la linea base. 
    
    """
    idlineabase = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80, null=True, blank=False)
    fase = models.ForeignKey(Fase)
    #genera una segunda tabla para las relaciones con el item
    items = models.ManyToManyField(Item)
    fechacreacion = models.DateField(auto_now=True, null=True )


#Solicitud

