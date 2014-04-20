from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand 
from projectman.apps.admin.models import Proyecto, Fase
from projectman.apps.admin.models import LISTA_PERMISOS

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

            Permission.objects.create(codename=idpermiso,
                                       name=descripcion,
                                       content_type=content_type)

    def handle(self, *args, **options):
        
        self._crea_permisos()
