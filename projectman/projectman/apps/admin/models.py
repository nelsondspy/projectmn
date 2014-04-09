from django.db import models



class Proyecto (models.Model):
    """Modelo Proyecto"""
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
    
    

class Fase(models.Model): 
    """Modelo Fase"""
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

    def __unicode__(self):
        return self.nombre

"""Lista estatica de Permisos """
LISTA_PERMISOS = [('PROYECTO_CREAR','Crear Proyecto'),
                  ('PROYECTO_MODIF','Modificar Proyecto'),
                  ('PROYECTO_ELIM','Eliminar Proyecto'),
                  ('FASE_CREAR','Crear Fase'),
                  ('FASE_MODIF','Modificar Fase'),
                  ('FASE_ELIM','Eliminar Fase'),
                  ]
