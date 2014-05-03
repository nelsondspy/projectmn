from django.db import models
from django.core.urlresolvers import reverse
from datetime import date
 
from projectman.apps.admin.models import Fase


class ItemTipos(models.Model):
    """
    
    Modelo ItemTipos : agrupan tipos de atributos. 
    -un tipo de item depende de la existencia de una fase

    """

    idtipoitem = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40 , blank=False , help_text='Nombre', null=False)
    descripcion = models.CharField(max_length=80, null=True, blank=True ,help_text='Descripcion')
    es_supertipo = models.BooleanField( default=False)
    #claves foraneas    null=False, blank=False 
    idfase = models.ForeignKey(Fase, blank=False, null=True )
    
    
    def __unicode__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('tipoitem_editar', kwargs={'pk': self.pk})


class ItemAtributos(models.Model):
    """ 
    
    ItemAtributos, un atributo tiene un nombre es un tipo de valor.
    -un tipo de atributo depende de un tipo de item
    
    """
    T_CHAR ='C'
    T_NUM ='N'
    T_DATE='D'

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
    E_ELIMINADO = 'ELI'
    
    
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
    estado = models.CharField(max_length=3, default=E_DESAPROBADO)
    version = models.IntegerField(default=0)
    #relaciones 
    idfase = models.ForeignKey(Fase) #idfase_id 
    idtipoitem = models.ForeignKey(ItemTipos)
    
    
    def sigte_numero(self):
        #ultimo = Item.objects.filter(idfase=self.idfase).order_by('numero')[0]
        ultimo = Item.objects.filter(idfase=self.idfase).count()
        if ultimo: 
            self.numero = ultimo + 1
        else:
            self.numero = 1

    def __unicode__(self):
        return self.nombre
    
    


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
    
    def set_valor_default(self):
        if self.idatributo.tipodato == ItemAtributos.T_DATE:
            self.valor = date.strftime(date.today(), "%d/%m/%Y")
            
        if self.idatributo.tipodato == ItemAtributos.T_NUM :
            self.valor = '0'
            
        if self.idatributo.tipodato == ItemAtributos.T_CHAR :
            self.valor = '--'
        
        



def carga_atributos_comunes():
    #Los atributos comunes a todos los items son de un tipo de item SIN fase
    tipo_defecto = ItemTipos()
    tipo_defecto.nombre='Default'
    tipo_defecto.descripcion='Atributos por defecto'
    tipo_defecto.es_supertipo=True
    tipo_defecto.save()
    #atributos de item
    attr1 = ItemAtributos(nombre='complejidad',tipodato='N',idtipoitem=tipo_defecto)
    attr1.save()
    
    attr2= ItemAtributos(nombre='prioridad',tipodato='N',idtipoitem=tipo_defecto)
    attr2.save()



class ItemRelacion(models.Model):
    """
    
    :Model: ItemRelacion 
    Modelo que permite almacenar las relaciones entre items.
    Items de una misma fase.
    Items de fases antecesoras.
    
    """
    #Estado de una relacion 
    E_ELIMINADO = 'DEL'
    E_ACTIVO = 'ACT'
    ESTADOS = ((E_ELIMINADO, 'Eliminado'),(E_ACTIVO, 'Activo'))
    #Tipo de relacion : interno (Intrafase) o externa(InterFase)
    E_INT = 'I'
    E_EXT = 'E'
    TIPOS = ((E_INT,'Padre -> Hijo'),(E_EXT,'Antecesor -->> Sucesor'))
    
    idrelacion = models.AutoField(primary_key=True)
    origen = models.ForeignKey(Item, related_name="origen")
    destino = models.ForeignKey(Item,related_name="destino")
    tipo=models.CharField(max_length=3, choices=TIPOS)
    estado = models.CharField(max_length=3, default=E_ACTIVO, choices=ESTADOS)
    
    def set_tipo(self):
        if self.origen.idfase_id == self.destino.idfase_id:
            self.tipo = self.E_INT
        else:
            self.tipo = self.E_EXT


class ItemAdjuntos(models.Model):
    """
    
    Archivos adjuntos del item.
    
    """
    idadjunto = models.AutoField(primary_key=True)
    archivo = models.FileField(upload_to='upl')
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    item = models.ForeignKey(Item)
    