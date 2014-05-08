from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views.view_comite import CrearComiteProyectoView ,ListarComiteProyectoView, EliminarMiembroView
from views.view_lineabase import CreaLineaBase 
from views.view_lineabase import ListarLineaBaseView
from views.view_solicitud import CreaSolicitudView ,ListaSolicitudesView


urlpatterns = patterns('projectman.apps',
    #comite 
    url(r'^comite/crear/(?P<idproyecto>\d+)$', login_required(CrearComiteProyectoView.as_view()), name="comite_crear"),
    url(r'^comite/listar/(?P<idproyecto>\d+)$', login_required(ListarComiteProyectoView.as_view()), name="comite_listar"),
    url(r'^comite/miembro/eliminar/(?P<pk>\d+)$', login_required(EliminarMiembroView.as_view()), name="comite_eliminar"),
    #linea base
    url(r'^lineabase/crear/(?P<idfase>\d+)$', login_required(CreaLineaBase.as_view()), name='linea_base_item_crear'),
    url(r'^lineabase/listar/(?P<idfase>\d+)$', login_required(ListarLineaBaseView.as_view()), name="lineabase_listar"),
    url(r'^lineabase/listar/(?P<idfase>\d+)/(?P<idlineabase>\d+)$', login_required(ListarLineaBaseView.as_view()), name="lineabase_listardetalle"), 
    url(r'^lineabase/listatabla/(?P<idfase>\d+)$', login_required(ListarLineaBaseView.as_view(template_name='gestcambio/lista_lineabase_plano.html')),\
         name="lineabase_listartabla") ,
    #solicitud de cambio
    url(r'^solicitud/crear/(?P<idlinebase>\d+)$', login_required(CreaSolicitudView.as_view()) , name="solicitud_crear" ),
    url(r'^solicitud/listar/(?P<idfase>\d+)$', login_required(ListaSolicitudesView.as_view()) , name="solicitudes_fase" ),
    url(r'^solicitud/items/(?P<idfase>\d+)/(?P<idsolicitud>\d+)$', login_required(ListaSolicitudesView.as_view()) , name="solicitud_det_item" ), 


)
