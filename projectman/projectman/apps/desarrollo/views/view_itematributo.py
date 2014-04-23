from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView 
from django.core.urlresolvers import reverse

from ..models import ItemAtributos
from ..models import ItemTipos
from ..forms import AtributosTiposForm


TEMPL_ATRIBUTOSFORM = 'desarrollo/form_atributos.html'
TEMPL_ATRIBUTOS_LIST = 'desarrollo/lista_atributos.html'


class CreaItemAtributoView(CreateView):
    """
    
    Crea un atributo en un tipo de item.
    -Recibe como parametros el identificador del tipo de item.
    -Retorna el template con el formulario para cargar los datos del atributo.
    -Persiste los datos del nuevo atributo.
    -Redirecciona a la vista que muestra el item con sus atributos.
    
    """
    model = ItemAtributos
    template_name = TEMPL_ATRIBUTOSFORM
    form_class = AtributosTiposForm
    param_fase = None
    templ_base_error = None 
    
    def get_success_url(self):
        return reverse('tipoitem_attr', kwargs={'idtipoitem':self.kwargs['idtipoitem'], 
                                                'idfase' : self.param_fase.idfase })
    
    def get_initial(self):
        itemtipo = get_object_or_404(ItemTipos, pk=self.kwargs['idtipoitem'])
        self.param_fase = itemtipo.idfase
        return { 'idtipoitem': itemtipo }
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('itematributo_crear',kwargs={'idtipoitem':self.kwargs['idtipoitem'] })
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)


class EditaItemAtributoView(UpdateView):
    """
    
    Modifica un atributo en un tipo de item.
    -Recibe como parametros el identificador del tipo de item.
    -Retorna el template con el formulario para editar los datos del atributo.
    -Persiste los cambios realizados en el atributo.
    
    """
    model = ItemAtributos
    template_name = TEMPL_ATRIBUTOSFORM
    form_class = AtributosTiposForm
    templ_base_error = None
    
    def get_success_url(self):
        return self.request.META['HTTP_REFERER']
    
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('itematributo_editar',kwargs={'pk':self.kwargs['pk'] })
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)


class ListaItemAtributoView(ListView):
    """
    
    Lista los atributos de un tipo de item. 
    
    """
    model= ItemAtributos 
    template_name= TEMPL_ATRIBUTOS_LIST
    item_param = None
    
    def get_queryset(self):
        self.item_param = ItemTipos.objects.get(pk=self.kwargs['idtipoitem'])
        return ItemAtributos.objects.filter(idtipoitem=self.item_param)
    #Obtiene la fase para imprimir sus datos en el template  
    def get_context_data(self, **kwargs):
        context = super(ListaItemAtributoView, self).get_context_data(**kwargs)
        context['tipoitem'] = self.item_param
        return context


class EliminaItemAtributoView(DeleteView):
    """
    
    Elimina un atributo .
    Recibe como parametro el identificador del atributo
    Solicita confirmacion para borrar el atributo
    
    """
    model= ItemAtributos
    template_name = 'form_confirm_delete.html'
    
    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('itematributo_eliminar',kwargs={'pk':self.kwargs['pk']})
        return context
