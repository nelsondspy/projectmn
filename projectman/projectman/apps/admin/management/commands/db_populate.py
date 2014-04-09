from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand 
from projectman.apps.admin.models import Proyecto
from projectman.apps.admin.models import LISTA_PERMISOS

class Command(BaseCommand): 
    args = '<foo bar ...>'
    help = 'our help string comes here'
    
    def _crea_permisos(self):
        Permission.objects.all().delete()
        content_type = ContentType.objects.get_for_model( Proyecto)
        for (idpermiso, descripcion) in LISTA_PERMISOS:
            Permission.objects.create(codename=idpermiso,
                                       name=descripcion,
                                       content_type=content_type)

    
    def handle(self, *args, **options):
        
        self._crea_permisos()
