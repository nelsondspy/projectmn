from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views.view_comite import CrearComiteProyectoView ,ListarComiteProyectoView
from views.view_lineabase import CargaLineaBaseItem

urlpatterns = patterns('projectman.apps',
    #gestion de tipos de items 
    url(r'^comite/crear/(?P<idproyecto>\d+)$', login_required(CrearComiteProyectoView.as_view()), name="comite_crear"),
    url(r'^comite/listar/(?P<idproyecto>\d+)$', login_required(ListarComiteProyectoView.as_view()), name="comite_listar"),
    url(r'^lineabase/(?P<idfase>\d+)$', login_required(CargaLineaBaseItem.as_view()), name='linea_base_item_crear')

)
