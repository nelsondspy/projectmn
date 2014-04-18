from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import CreaItemTipoView, EditaItemTipoView, ListaItemTipoView, EliminaItemTipoView
from views import CreaItemAtributoView, ListaItemAtributoView, EditaItemAtributoView, EliminaItemAtributoView


urlpatterns = patterns('projectman.apps',
    url(r'^$', 'desarrollo.views.mostrar_panel'),
    url(r'^componentes/(?P<idproyecto>\d+)/$', 'desarrollo.views.editor_componentes', name='editor_componentes'),
    url(r'^componentes/(?P<idproyecto>\d+)/(?P<idfase>\d+)$', 'desarrollo.views.editor_componentes'),
    url(r'^procesaitem/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'desarrollo.views.procesa_item'),
    url(r'^procesaitem/$', 'desarrollo.views.procesa_item'),
    #gestion de tipos de items 
    url(r'^tipoitem/editar/(?P<pk>\d+)$', login_required(EditaItemTipoView.as_view()), name="tipoitem_editar"),
    url(r'^tipoitem/crear/(?P<idfase>\d+)$', login_required(CreaItemTipoView.as_view()), name="tipoitem_crear"),
    url(r'^tipoitem/lista/(?P<idfase>\d+)$', login_required(ListaItemTipoView.as_view()), name="tipoitem_lista"),
    url(r'^tipoitem/attr/(?P<idfase>\d+)/(?P<idtipoitem>\d+)$', login_required(ListaItemTipoView.as_view()), name="tipoitem_attr"),
    url(r'^tipoitem/eliminar/(?P<pk>\d+)$', login_required(EliminaItemTipoView.as_view()), name="tipoitem_eliminar"),
    #gestion de atributos
    url(r'^atributos/crear/(?P<idtipoitem>\d+)$', login_required(CreaItemAtributoView.as_view()),name="itematributo_crear"),
    url(r'^atributos/editar/(?P<pk>\d+)$', login_required(EditaItemAtributoView.as_view()),name="itematributo_editar"),
    url(r'^atributos/lista/(?P<idtipoitem>\d+)$', login_required(ListaItemAtributoView.as_view()),name="itematributo_lista"),
    url(r'^atributos/eliminar/(?P<pk>\d+)$', login_required(EliminaItemAtributoView.as_view()),name="itematributo_eliminar")
)
