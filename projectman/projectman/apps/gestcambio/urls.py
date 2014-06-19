from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views.view_comite import CrearComiteProyectoView ,ListarComiteProyectoView, EliminarMiembroView
from views.view_lineabase import CreaLineaBase
from views.view_lineabase import ListarLineaBaseView
#from views.view_solicitud import CreaSolicitudView ,ListaSolicitudesView, SetSolicitudEnviada, EditaSolicitudView, EliminaSolicitudView ,DetalleSolicitud , SetSolicitudEjecutada
from views.view_solicitud import *
from views.view_solicitudvoto import ListaSolicPendientes, VotaSolicitudView, EstadoVotacionView
from views.view_reportes import ListaSolicitudesPDF , ListaSolicForm


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
    url(r'^solicitud/listaproyecto/(?P<idproyecto>\d+)$', login_required(ListaSolicitudesView.as_view()) , name="solicitudes_proyecto" ),
    url(r'^solicitud/mis_solicitudes/(?P<idproyecto>\d+)/(?P<missolicitudes>\d+)$', login_required(ListaSolicitudesView.as_view()) , name="solicitudes_usuario" ),
    url(r'^solicitud/items/(?P<pk>\d+)$', login_required(DetalleSolicitud.as_view()) , name="solicitud_det_item" ),
    url(r'^solicitud/enviar/(?P<pk>\d+)$', login_required(SetSolicitudEnviada.as_view()) , name="solicitud_envia" ) ,
    url(r'^solicitud/editar/(?P<pk>\d+)$', login_required(EditaSolicitudView.as_view()) , name="solicitud_edita" ),
    url(r'^solicitud/eliminar/(?P<pk>\d+)$', login_required(EliminaSolicitudView.as_view()) , name="solicitud_eliminar" ),
    url(r'^solicitud/terminar/(?P<pk>\d+)$', login_required(SetSolicitudEjecutada.as_view()) , name="solicitud_terminar" ) ,

    url(r'^solicitudes/pendientes/(?P<idproyecto>\d+)$', login_required(ListaSolicPendientes.as_view()) , name="solicitudes_pend_proy" ),
    url(r'^solicitudes/votar/(?P<pk>\d+)/(?P<accion>[a-z]+)$', login_required(VotaSolicitudView.as_view()) , name="solicitud_votar" ),
    url(r'^solicitud/estadovotacion/(?P<idsolicitud>\d+)$', login_required(EstadoVotacionView.as_view()) , name="solicitud_est_votacion" ),

    #reportes:formulario de reportes y listados pdf 
    url(r'^solicitudes/reporte_pdf$', login_required(ListaSolicitudesPDF.as_view()) , name="solicreport_pdf"),
    url(r'^solicitudes/reporte/(?P<idproyecto>\d+)$', login_required(ListaSolicForm.as_view()) , name="solicreport_form")
)
