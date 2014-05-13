from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission



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

    def __unicode__(self):
        return self.nombre
    

    

class Fase(models.Model): 
    """Modelo Fase"""
    E_INICIAL = 'INI'
    E_DESARROLLO = 'DES'
    E_FINALIZADO = 'FIN'
    
    ESTADOS=(
        (E_INICIAL, 'Inicial'),
        (E_DESARROLLO, 'Desarrollo'),
        (E_FINALIZADO, 'Finalizado')
    )
    idfase = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=40, null=False, blank=False,
         help_text='Nombre de la fase' , verbose_name='Nombre de la fase')
    descripcion = models.CharField(max_length=80 , verbose_name='Descripcion' , blank=True)
    idproyecto = models.ForeignKey(Proyecto)
    estado = models.CharField(max_length=3, choices=ESTADOS, default=E_DESARROLLO)
    fechacreacion = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.nombre

"""Lista estatica de Permisos """
LISTA_PERMISOS = [
                  #permisos no asociados a objetos particulares
                  ('usuario_crear', 'Crear Usuario', 0),
                  ('usuario_modif', 'Modificar datos del usuario', 0),
                  ('usuario_elim', 'Eliminar usuario', 0),
                  ('rol_crear', 'Crear Rol', 0),
                  ('rol_elim', 'Eliminar Rol', 0),
                  ('rol_modif', 'Modificar Rol', 0),
                  ('rol_asignar', 'Asignar Rol', 0),
                  ('proyecto_crear', 'Crear Proyecto', 0),
                  #permisos asociados a proyectos especificos 
                  ('proyecto_modif', 'Modificar Proyecto', 1),
                  ('proyecto_elim', 'Eliminar Proyecto', 1),
                  ('proyecto_iniciar', 'Iniciar Proyecto', 1),
                  ('fase_crear', 'Crear Fase', 1),
                  ('relacion_crear', 'Relacionar items', 1),
                  ('relacion_elim', 'Eliminar relaciones entre items', 1),
                  ('comite_gest', 'Gestionar comite de cambios', 1),
                  #permisos asociados a fases especificas
                  ('fase_modif', 'Modificar Fase', 2), 
                  ('fase_elim', 'Eliminar Fase', 2),
                  ('tipoitem_gestion', 'Gestionar tipos de item', 2),
                  ('item_crear', 'Crear Item', 2),
                  ('item_modif', 'Modificar Item', 2),
                  ('item_elim', 'Eliminar Item', 2),
                  ('item_revivir', 'Revivir Item', 2),
                  ('lineabase_crear', 'Crear Linea Base', 2)
                  ] 


class RolProyecto(models.Model):
    """
    
    Almacena informacion de los roles asignados a proyectos y fases.
    La aplicacion de django-auth es insuficiente ya que no provee seguridad
    a nivel a instancias particulares de objetos.
    
    """
    idrolproyecto = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Group)
    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)

        
    def __unicode__(self):
        return ('usuario:'+ self.usuario.__unicode__() + 
                ', rol: ' + self.rol.__unicode__() + 
                ', proyecto:'+ self.proyecto.__unicode__())
    
    
class RolFases(models.Model):
    """

    Fases sobre las que se asignan los permisos por roles
    
    """
    idrolfase = models.AutoField(primary_key=True)
    fase = models.ForeignKey(Fase)
    rolproyecto = models.ForeignKey(RolProyecto)

    def __unicode__(self):
        return ('Permisos a la fase : '+ self.fase.__unicode__())


def exist_permiso_proyecto(idusuario, idproyecto, idpermiso ):
    """
    
    Verifica la existencia de una permiso para un usuario y proyecto. 
    
    """
    #django crea un atributo para cada clave foranea con el sujito _id 
    relacion = RolProyecto.objects.filter(usuario_id=idusuario).filter(proyecto_id=idproyecto)
    permisos = Permission.objects.filter(group__rolproyecto__in=relacion).filter(codename=idpermiso)
    return (permisos.count() > 0)


def exist_permiso(idusuario, idpermiso):
    """
    
    Verifica la existencia de una permiso para un usuario. 
    
    """ 
    #django crea un atributo para cada clave foranea con el sujito _id 
    relacion = RolProyecto.objects.filter(usuario_id=idusuario)
    permisos = Permission.objects.filter(group__rolproyecto__in=relacion).filter(codename=idpermiso)
    return (permisos.count() > 0)


def exist_permiso_fase(idusuario, idfase, idpermiso):
    """
    
    Verifica la existencia de una permiso para un usuario y una fase
    
    """
    relacion = RolProyecto.objects.filter(usuario_id=idusuario).filter(
                            rolfases__fase_id=idfase)
    permisos = Permission.objects.filter(group__rolproyecto__in=relacion).filter(codename=idpermiso)

    return (permisos.count() > 0)
