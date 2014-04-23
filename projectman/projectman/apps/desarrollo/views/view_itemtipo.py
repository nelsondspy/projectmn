from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import  get_object_or_404
from django.views.generic import ListView 
from django.core.urlresolvers import reverse
from projectman.apps.admin.models import  Fase

from ..models import ItemTipos
from ..models import ItemAtributos
from ..forms import ItemTiposForm

TEMPL_ITEMTIPFORM = 'desarrollo/form_itemtipos.html'
TEMPL_ITEMTIPO_LIST = 'desarrollo/lista_itemtipos.html'


class ListaItemTipoView(ListView):
    """
    
    Lista los  tipos de items de una fase.
    Lista los atributos de un tipo de item seleccionado
    
    """
    model= ItemTipos
    template_name= TEMPL_ITEMTIPO_LIST
    fase_param = None
    ob_tipoitem = None
    ls_atributos = None
    
    def get_queryset(self):
        self.fase_param = get_object_or_404(Fase,pk=self.kwargs['idfase'] )
        if self.kwargs.get('idtipoitem'):
            self.ob_tipoitem = get_object_or_404(ItemTipos, pk=self.kwargs['idtipoitem'] )
            self.ls_atributos = ItemAtributos.objects.filter(idtipoitem=self.ob_tipoitem)
            
        return ItemTipos.objects.filter(idfase=self.fase_param)
    #Obtiene la fase para imprimir sus datos en el template  
    def get_context_data(self, **kwargs):
        context = super(ListaItemTipoView, self).get_context_data(**kwargs)
        context['fase'] = self.fase_param
        context['ls_atributos'] = self.ls_atributos
        context['idtipoitem'] = int(self.kwargs.get('idtipoitem',0))
        return context


class CreaItemTipoView(CreateView):
    """
    
    Crea un tipo de item.
    
    """
    model= ItemTipos
    template_name = TEMPL_ITEMTIPFORM
    form_class = ItemTiposForm
    fase_param = None
    templ_base_error = None
    
    def get_success_url(self):
        return reverse('tipoitem_lista',kwargs={'idfase':self.kwargs['idfase']})
    
    def get_initial(self):
        fase = Fase.objects.get(pk=self.kwargs['idfase'])
        return { 'idfase': fase }

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('tipoitem_crear',kwargs={'idfase':self.kwargs['idfase'] })
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)



class EditaItemTipoView(UpdateView):
    """
    
    Edita un tipo de item
    
    """
    model= ItemTipos
    template_name = TEMPL_ITEMTIPFORM
    form_class = ItemTiposForm
    templ_base_error = None
    
    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('tipoitem_editar', kwargs={'pk':self.kwargs['pk'] })
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)



class EliminaItemTipoView(DeleteView):
    """
    
    Elimina un tipo de item.
    Recibe como parametro el identificador del tipo de item
    Solicita confirmacion para borrar el item 
    
    """
    model= ItemTipos
    template_name = 'form_confirm_delete.html'
    
    
    def get_success_url(self):
        #redirige a la lista de items que posee la fase
        itemtipo = get_object_or_404(ItemTipos, pk=self.kwargs['pk'])
        fase_actual = (itemtipo.idfase).idfase
        return reverse('tipoitem_lista',kwargs={'idfase':fase_actual})

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('tipoitem_eliminar',kwargs={'pk':self.kwargs['pk']})
        return context
