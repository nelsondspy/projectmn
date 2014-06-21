from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand 
from projectman.apps.admin.models import Proyecto, Fase
from projectman.apps.admin.models import LISTA_PERMISOS
from django.contrib.auth.models import Group 
from django.contrib.auth.models import Permission
from projectman.apps.admin.models import RolProyecto , RolFases


class Command(BaseCommand): 
    args = ''
    help = ''
    
    def _crea_permisos(self):
        """
        
        inserta los permisos en la base de datos.
        Los modelos asignados son solo requerimiento del framework. De todas 
        formas se asigno el modelo acorde a su nivel.  
        
        """
        
        Permission.objects.all().delete()
        
        for (idpermiso, descripcion, nivel) in LISTA_PERMISOS:
            if nivel == 0 :
                content_type = ContentType.objects.get_for_model(User)
            if nivel == 1 :
                content_type = ContentType.objects.get_for_model(Proyecto)
            if nivel == 2:
                content_type = ContentType.objects.get_for_model(Fase)
            
            try:
                Permission.objects.create(codename=idpermiso,
                                       name=descripcion,
                                       content_type=content_type)
            except:
                print 'permiso ya existe'

    def handle(self, *args, **options):
        
        self._crea_permisos()
        #self.crear_componentes_proyecto1()
    
    def crear_componentes_proyecto1(self):
        #crea usuarios 
        nelsond = User.objects.create_user('nelsond', 'nelson@gmail.com', '12345')
        ariel = User.objects.create_user('arielm', 'ariel@gmail.com', '32145')

        #crea proyectos 
        proyecto1 = None
        #crea fases
        fase1 = None 

        #crea roles 
        desarrollador = Group(name="desarrollador")
        desarrollador.permissions= [Permission.objects.get('proyecto_crear'),\
                                    Permission.objects.get('proyecto_modif'),\
                                     ]
        
        #asigna un proyecto a un usuario
        rolproyecto = RolProyecto(proyecto = proyecto1, usuario= ariel)
        #asignar una fase a un proyecto_usuario
        RolFases(rolproyecto =rolproyecto, fase = fase1 )
        
        



