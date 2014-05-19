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
    incorporacion = models.DateField(auto_now=True)

    
    def __unicode__(self):
        return self.proyecto.__str__() +'..'+ self.usuario.__str__() 

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
    
    def __unicode__(self):
        return self.descripcion


#Solicitud
class SolicitudCambio(models.Model):
    """
    
    Modelo que almacena una solicitud de cambio.
    
    """
    E_ENVIADO = 'ENV'
    E_APROBADO ='APR'
    E_RECHAZADO = 'REC'
    E_BORRADOR = 'BOR'
    #indica que la solicitud fue aplicada
    E_TERMINADO = 'TER'

    ESTADOS = (
        (E_ENVIADO, 'Enviado'),
        (E_APROBADO, 'Aprobado'),
        (E_RECHAZADO, 'Rechazado'),
        (E_BORRADOR, 'Borrador'),
        #indica que la solicitud fue aplicada 
        (E_TERMINADO, 'Terminado')
    )

    idsolicitud =  models.AutoField(primary_key=True)
    comentarios = models.CharField(max_length=120, null=True, blank=False)
    solicitante = models.ForeignKey(User)
    #los items pertenecen solo a una linea base 
    items = models.ManyToManyField(Item)
    lineabase = models.ForeignKey(LineaBase)
    estado = models.CharField(max_length=3, default=E_BORRADOR)
    fecha_aprobacion =  models.DateField(null=True )
    fecha_creacion =  models.DateField(auto_now=True,blank=False, null=False)
    
    def __unicode__(self):
        return self.solicitante
    
class CambioTipos(models.Model):
    """
    
    Tipo de cambio de la solicitud. 
    
    """
    idtipocambio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, null=True, blank=False)

