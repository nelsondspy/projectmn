from django.conf.urls import patterns, url

from views import ListaPermisosView
from views import CreaUsuarioView
from views import ListarUsuarioView
from views import CreaRolPermisosView
from views import EditaRolPermisosView
from views import ListaRolPermisosView
from views import EliminaRolPermisosView
from views import EliminarUsuarioView
from views import EditaUsuarioView
from views import EditaUsuarioRoles
from views import ConsultaUsuarioView

urlpatterns = patterns('projectman.apps',
    url(r'^autenticar/$', 'admin.views.autenticar'),
    url(r'^cerrar_sesion/$', 'admin.views.cerrar_sesion', name='cerrar_sesion'),
    url(r'^login/$', 'admin.views.login_form'),
    
    url(r'^proyectos/$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<accion>[a-z]+)/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^fases/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'admin.views.fases_abm'),
    url(r'^fases/$', 'admin.views.fases_abm'),
    url(r'^permisos/lista/(?P<pk>\d+)$',ListaPermisosView.as_view(), name="permisos_lista"),
    
    url(r'^usuario/crear$', CreaUsuarioView.as_view(), name='usuario_crear'),
    url(r'^usuario/listar$', ListarUsuarioView.as_view(), name='usuario_listar'),
    url(r'^usuario/eliminar/(?P<pk>\d+)$',EliminarUsuarioView.as_view(), name='usuario_elimina'),
    url(r'^usuario/editar/(?P<pk>\d+)$',EditaUsuarioView.as_view(), name='usuario_edita'),
    url(r'^usuario/editaroles/(?P<pk>\d+)$',EditaUsuarioRoles.as_view(), name='usuario_editaroles'),
    url(r'^usuario/detalle/(?P<pk>\d+)$',ConsultaUsuarioView.as_view(), name='usuario_detalle'),
        
    url(r'^rol/crear/$', CreaRolPermisosView.as_view(), name='rol_permisos'),
    url(r'^rol/editar/(?P<pk>\d+)$', EditaRolPermisosView.as_view(), name='rol_permisos_edita'),
    url(r'^rol/lista/$', ListaRolPermisosView.as_view(), name='rol_permisos_lista'),
    url(r'^rol/eliminar/(?P<pk>\d+)/$', EliminaRolPermisosView.as_view(), name='rol_permisos_elimina') 
)
