from django.conf.urls import patterns, url,include

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
from views import AsignaRolProyectoView
from views import ListaRolProyectoView
from views import EliminaRolProyectoView
from views import ListaProyectosUsuario
from views import AsignaFaseRolView
from views import EliminaRolFaseView
from views import ListaRolFasesView
from views import IniciarProyecto
from views import FinalizaFase

urlpatterns = patterns('projectman.apps',
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^autenticar/$', 'admin.views.autenticar'),
    url(r'^cerrar_sesion/$', 'admin.views.cerrar_sesion', name='cerrar_sesion'),
    url(r'^login/$', 'admin.views.login_form'),
    
    url(r'^proyectos/$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<accion>[a-z]+)/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/crear/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm' ,name='proyecto_crear'),
    url(r'^proyectos/editar/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm' ,name='proyecto_editar'),
    url(r'^proyectos/eliminar/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm' ,name='proyecto_eliminar'),

    
    url(r'^fases/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'admin.views.fases_abm'),

    url(r'^fases/eliminar/(?P<idelemento>\d+)$', 'admin.views.fases_abm', name="fases_eliminar"),
    url(r'^fases/editar/(?P<idelemento>\d+)$', 'admin.views.fases_abm', name="fases_editar"),
    url(r'^fases/crear/(?P<idelemento>\d+)$', 'admin.views.fases_abm', name="fases_crear"),

    url(r'^fases/$', 'admin.views.fases_abm', name="fases_abm"),
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
    url(r'^rol/eliminar/(?P<pk>\d+)/$', EliminaRolPermisosView.as_view(), name='rol_permisos_elimina'),
    
    url(r'^rol/asignar/$', AsignaRolProyectoView.as_view(), name='rol_proyecto_crear'),
    url(r'^rol/listaasignados/$', ListaRolProyectoView.as_view(), name='rol_proyecto_listar'),
    url(r'^rol/listaasignados/(?P<idrolproyecto>\d+)$', ListaRolProyectoView.as_view(), name='rol_proyecto_fase'),
    
    url(r'^rol/desasignar/(?P<pk>\d+)$', EliminaRolProyectoView.as_view(), name='rol_proyecto_eliminar'),
    url(r'^rol/asignarfase/(?P<idrolproyecto>\d+)$', AsignaFaseRolView.as_view(), name='rol_fase_crear'), 
    url(r'^rol/eliminarfase/(?P<pk>\d+)$', EliminaRolFaseView.as_view(), name='rol_fase_eliminar'),
    url(r'^rol/listarfases/(?P<idrolproyecto>\d+)$', ListaRolFasesView.as_view(), name='rol_fase_listar'), 
    #lista los proyectos asignados al usuario
    url (r'^proyectos/listaasig$', ListaProyectosUsuario.as_view(), name='proyectos_asignados'),
    url (r'^proyecto/iniciar/(?P<pk>\d+)$', IniciarProyecto.as_view(), name='iniciar_proyecto'),
    #finalizar fase 
    url (r'^fase/finalizar/(?P<pk>\d+)$', FinalizaFase.as_view(), name='finalizar_fase')
)
