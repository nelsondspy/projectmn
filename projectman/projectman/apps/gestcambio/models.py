from django.db import models
from ..admin.models import Proyecto 
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

#LineaBaseItem

#Solicitud

