from django.db import models


"""Modelo Proyecto"""
class Proyecto (models.Model):
    E_NOINICIADO='NOI'
    E_INICIADO='INI'
    E_FINALIZADO='FIN'
    ESTADOS=(
        (E_NOINICIADO, 'No-iniciado'),
        (E_INICIADO, 'Iniciado'),
        (E_FINALIZADO, 'Finalizado')
    )
    idproyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, null=False, blank=False,
         help_text='Nombre del proyecto' , verbose_name='Nombre del proyecto')
    descripcion = models.CharField(max_length=80 , verbose_name='Descripcion' ,null=True, blank=True)
    fechainicio = models.DateField(verbose_name='Fecha Inicio', null=True)
    fechafin = models.DateField(verbose_name='Fecha finalizacion',null=True)
    estado = models.CharField(max_length=3, choices=ESTADOS)
    
    

"""Modelo Fase"""
class Fase(models.Model):
    E_INICIAL = 'INI'
    E_DESARROLLO = 'DES'
    E_COMPLETO = 'COM'
    E_FINALIZADO = 'FIN'
    
    ESTADOS=(
        (E_INICIAL, 'Inicial'),
        (E_DESARROLLO, 'Desarrollo'),
        (E_COMPLETO, 'Completo'),
        (E_FINALIZADO, 'Finalizado')
    )
    idfase = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=40, null=False, blank=False,
         help_text='Nombre de la fase' , verbose_name='Nombre de la fase')
    descripcion = models.CharField(max_length=80 , verbose_name='Descripcion' , blank=True)
    idproyecto = models.ForeignKey(Proyecto)
    estado = models.CharField(max_length=3, choices=ESTADOS)
    fechacreacion = models.DateField(auto_now=True)

