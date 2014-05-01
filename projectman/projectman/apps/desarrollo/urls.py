from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views.view_itemtipo import CreaItemTipoView,EditaItemTipoView, ListaItemTipoView, EliminaItemTipoView
from views.view_itematributo import CreaItemAtributoView, ListaItemAtributoView, EditaItemAtributoView, EliminaItemAtributoView
from views.view_item import CreaItemView, SetEliminadoItemView, EditItemView
from views.view_itemvalores import AsignaValoresItem
from views.view_itemrelacion import CreaRelacionView, ListaRelacionesView, EliminaRelacionView

urlpatterns = patterns('projectman.apps',
    url(r'^$', 'desarrollo.views.view_oth.mostrar_panel'),
    url(r'^componentes/(?P<idproyecto>\d+)/$', 'desarrollo.views.view_oth.editor_componentes', name='editor_componentes'),
    url(r'^componentes/(?P<idproyecto>\d+)/(?P<idfase>\d+)$', 'desarrollo.views.view_oth.editor_componentes', name='expl_nivelfase'),
    url(r'^procesaitem/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'desarrollo.views.view_item.procesa_item', name='expl_nivelitem'),
   
    #
    url(r'^item/crear/(?P<idfase>\d+)$', login_required(CreaItemView.as_view()), name='item_crear' ),
    url(r'^item/eliminar/(?P<pk>\d+)$', login_required(SetEliminadoItemView.as_view()), name='item_eliminar' ), 
     url(r'^item/modificar/(?P<pk>\d+)$', login_required(EditItemView.as_view()), name='item_editar' ), 
    
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
    url(r'^atributos/eliminar/(?P<pk>\d+)$', login_required(EliminaItemAtributoView.as_view()),name="itematributo_eliminar") ,
    #gestion de valores de items 
    url(r'^item/asignarvalores/(?P<iditem>\d+)$', AsignaValoresItem.as_view(), name="valores_asignar") ,
    #relaciones 
    url(r'^relacion/crear/(?P<idproyecto>\d+)$', CreaRelacionView.as_view(), name="relacion_crear"),
    url(r'^relaciones/listar/(?P<idproyecto>\d+)$', ListaRelacionesView.as_view(), name="relacion_listar"),
    url(r'^relacion/eliminar/(?P<pk>\d+)$', EliminaRelacionView.as_view(), name='relacion_eliminar'),
    
)
