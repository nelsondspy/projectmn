from django.conf.urls import patterns, url

from views import ListaPermisosView

from views import CreaUsuarioView
from views import ListarUsuarioView
from views import CreaRolPermisosView
from views import EditaRolPermisosView
from views import ListaRolPermisosView
from views import EliminaRolPermisosView

urlpatterns = patterns('projectman.apps',
    url(r'^autenticar/$', 'admin.views.autenticar'),
    url(r'^cerrar_sesion/$', 'admin.views.cerrar_sesion'),
    url(r'^login/$', 'admin.views.login_form'),
    url(r'^proyectos/$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<accion>[a-z]+)/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^fases/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'admin.views.fases_abm'),
    url(r'^fases/$', 'admin.views.fases_abm'),
    url(r'^permisos/lista$',ListaPermisosView.as_view(), name="permisos_lista"),
    url(r'^usuario/crear$', CreaUsuarioView.as_view(), name='usuario_crear'),
    url(r'^usuario/listar$', ListarUsuarioView.as_view(), name='usuario_listar'),
    url(r'^rol/crear/$', CreaRolPermisosView.as_view(), name='rol_permisos'),
    url(r'^rol/editar/(?P<pk>\d+)$', EditaRolPermisosView.as_view(), name='rol_permisos_edita'),
    url(r'^rol/lista/$', ListaRolPermisosView.as_view(), name='rol_permisos_lista'),
    url(r'^rol/eliminar/(?P<pk>\d+)/$', EliminaRolPermisosView.as_view(), name='rol_permisos_elimina')
)
