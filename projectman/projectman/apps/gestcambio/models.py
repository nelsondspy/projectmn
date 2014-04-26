from django.db import models
from ..admin.models import Proyecto
from  ..admin.models import Fase
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
    idlineabase = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80, null=True, blank=True)
    fase = models.ForeignKey(Fase)
    

class LineaBaseItem(models.Model):
    idlbitem = models.AutoField(primary_key=True)
    lineabase = models.ForeignKey(LineaBase)

#Solicitud

