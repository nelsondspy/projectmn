from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView 
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages 

from ..models import ItemRelacion, Item 
from projectman.apps.admin.models import Proyecto, Fase

from ..forms import ItemRelacionForm

TEMPL_RELACION_FORM = 'desarrollo/form_relacion.html'
TEMPL_RELACION_LISTA = 'desarrollo/lista_relaciones.html'


class CreaRelacionView(CreateView):
    """
    
    Vista que permite crear relaciones entre items.
    De una misma fase.
    De fases antecesoras. 
    
    """
    
    model = ItemRelacion
    template_name = TEMPL_RELACION_FORM
    form_class = ItemRelacionForm
    valido = True
    
    
    def get_success_url(self):
        return reverse('relacion_listar', kwargs={'idproyecto':self.kwargs['idproyecto']})
    
    def get_form(self, form_class):
        form = CreateView.get_form(self, form_class)
        #el selector solo debe desplegar los items del proyecto 
        fases = Fase.objects.filter(idproyecto_id=self.kwargs['idproyecto'])
        #lista los items que coinciden con las fases de proyecto 
        items = Item.objects.filter(idfase__in=fases)
        #cargamos los selectores con los items y mostrando a que fase pertenecen 
        opciones = [(item.pk,'['+ item.idfase.__str__()[0:5]+'..] ' +\
                     '[' + item.estado +']  | ' +
                      item.nombre[0:40] ) for item in items]
        form.fields['origen'].choices = opciones
        form.fields['destino'].choices = opciones
        return form
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('relacion_crear',\
                                kwargs ={'idproyecto' :self.kwargs['idproyecto'] })
        if not self.valido:
            context['nodefault'] = '__panel.html'
            
        return context
    
    def form_valid(self, form):
        #establece el tipo de la relacion , si es interna a la fase o externa
        # es decir padre e hijo o antecesor sucesor.
        form.instance.set_tipo()
        origen = form.instance.origen
        destino = form.instance.destino
        #Serie de validaciones 
        if valid_relacion_unica(origen, destino):
            messages.error(self.request, 'La relacion ya existe: ' + \
                           origen.__str__()+ ' --> '+ destino.__str__())
            self.valido = False
            return self.form_invalid(form)
        
        return CreateView.form_valid(self, form)
    
    def form_invalid(self, form):
        self.valido = False
        return CreateView.form_invalid(self, form)
    
    


def valid_relacion_unica(porigen, pdestino):
    """
    
    Valida que aun no exista la relacion.
    
    """
    relacion = ItemRelacion.objects.filter(Q(origen=porigen) & Q(destino=pdestino))
    return relacion.count()
                                
                                



class ListaRelacionesView(ListView):
    """
    
    Vista que consulta las relaciones a nivel de :
    -Fase.
    -Item.
    -Proyecto en general.
    
    """
    model = ItemRelacion
    template_name = TEMPL_RELACION_LISTA
    
    def get_queryset(self):
        
        #lista las relaciones que tiene una fase 
        if self.kwargs.get('idfase',None):
            object_list = None
        
        #lista todas las relaciones que implican ese item
        if self.kwargs.get('iditem',None):
            object_list = ItemRelacion.objects.filter().all()
            
        #lista todas las relaciones que implican ese item
        if self.kwargs.get('idproyecto',None):
            #No es optima esta consulta
            fases = Fase.objects.filter(idproyecto_id=self.kwargs.get('idproyecto'))
            items = Item.objects.filter(idfase__in=fases)
            
            object_list = ItemRelacion.objects.filter((Q(origen__in=items)|\
                                                       Q(destino__in=items)) &\
                                                    Q(estado=ItemRelacion.E_ACTIVO))
        return object_list
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['idproyecto'] = self.kwargs.get('idproyecto')
        return context 

