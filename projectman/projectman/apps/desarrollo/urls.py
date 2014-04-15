from django.conf.urls import patterns, url
from views import CreaItemTipoView, EditaItemTipoView, ListaItemTipoView
from views import CreaItemAtributoView, ListaItemAtributoView


urlpatterns = patterns('projectman.apps',
    url(r'^$', 'desarrollo.views.mostrar_panel'),
    url(r'^componentes/(?P<idproyecto>\d+)/$', 'desarrollo.views.editor_componentes', name='editor_componentes'),
    url(r'^componentes/(?P<idproyecto>\d+)/(?P<idfase>\d+)$', 'desarrollo.views.editor_componentes'),
    url(r'^procesaitem/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'desarrollo.views.procesa_item'),
    url(r'^procesaitem/$', 'desarrollo.views.procesa_item'),
    url(r'^tipoitem/(?P<pk>\d+)$', EditaItemTipoView.as_view(),name="tipoitem_editar"),
    url(r'^tipoitem/crear/(?P<idfase>\d+)$', CreaItemTipoView.as_view(),name="tipoitem_crear"),
    url(r'^tipoitem/lista/(?P<idfase>\d+)$', ListaItemTipoView.as_view(),name="tipoitem_lista"),
    url(r'^atributos/crear/(?P<idtipoitem>\d+)$', CreaItemAtributoView.as_view(),name="itematributo_crear"),
    url(r'^atributos/lista/(?P<idtipoitem>\d+)$', ListaItemAtributoView.as_view(),name="itematributo_lista"),
)


