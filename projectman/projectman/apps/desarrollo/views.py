from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView 
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
 
from projectman.apps.admin.models import  Proyecto, Fase

from models import ItemTipos, Item , ItemAtributos
 
from forms import ItemTiposForm, ItemForm, AtributosTiposForm

#nombres de variables de sesion 
SESS_IDPROYECTO = 'idproyecto'
SESS_IDFASE = 'idfase'

#nombres de templates 
TEMPL_PANEL = '__panel.html'
TEMPL_EXPLORADOR = 'explorador_comp.html'
TEMPL_ITEMTIPFORM = 'desarrollo/form_itemtipos.html'
TEMPL_ITEMTIPO_LIST = 'desarrollo/lista_itemtipos.html'
TEMPL_ATRIBUTOSFORM = 'desarrollo/form_atributos.html'
TEMPL_ATRIBUTOS_LIST = 'desarrollo/lista_atributos.html'

@login_required
def mostrar_panel(request):
    return render(request, TEMPL_PANEL)



def redirige_edicion_actual(request, nivel=0):
    """
    
    Redirige a la vista que muestra el proyecto/fase/item que se esta editando
    actualmente, segun las variables de sesion, por niveles de url 
    
    """

    #por defecto el nivel 0 es el proyecto
    url_redirigir = '/desarrollo/componentes/'+ request.session[SESS_IDPROYECTO]
    #el nivel 1 es la fase
    if nivel == 1: 
        url_redirigir  += '/'+request.session[SESS_IDFASE]
    #el nivel 2 es el item 
    return redirect(url_redirigir)


@login_required
def editor_componentes(request, idproyecto=None, idfase=None):
    """"
    
    Explorador de componentes de forma jerarquica permitira 
    -Listar fases, 
    -Los items de una fase
    -Los valores de atributos del item seleccionado 
    
    """

    proyecto = Proyecto.objects.get(pk=idproyecto)
    request.session[SESS_IDPROYECTO] = idproyecto
    request.session[SESS_IDFASE] = None
    #lista las fases del proyecto  
    lista_fases = Fase.objects.filter(idproyecto=idproyecto)
    #lista de items de una fase seleccionada ( recibida como parametro) 
    lista_items = None
    if idfase:
        request.session[SESS_IDFASE] = idfase
        lista_items = Item.objects.filter(idfase=idfase)
        idfase = int(idfase) # en la plantilla se requier el valor entero no el unicode
        
    return render(request , TEMPL_EXPLORADOR , {'proyecto': proyecto , 'idfase':idfase,
                    'lista_fases':lista_fases , 'lista_items':lista_items})


@login_required
def procesa_item(request, accion=None,idelemento=None):
    if accion in ('editar', 'eliminar', 'crear'):
        if accion == 'eliminar':
            item = Item.objects.get(pk=idelemento) 
            item.delete()
            return redirige_edicion_actual(request, nivel=1)
        if accion =='editar' :
            item  = Item.objects.get(pk=idelemento) 
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
        if accion == 'crear':
            fase = Fase.objects.get(pk=idelemento) 
            item = Item(idfase=fase)
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
    if request.method == 'POST':
        #Edita una fase existente, o crear unan nueva
        idfasepost = request.POST.get('idfase',None)
        iditempost = request.POST.get('iditem',None)
        if iditempost:
            instancia_item = Item.objects.get(pk=iditempost)
        if idfasepost:
            fase = Fase.objects.get(pk=idfasepost)
            instancia_item = Item(idfase=fase)
            instancia_item.sigte_numero()
        itemform = ItemForm(request.POST, instance=instancia_item)
        if itemform.is_valid():
            itemform.save()     
            return redirige_edicion_actual(request, nivel=1)


class ListaItemTipoView(ListView):
    """Lista tipos de items """
    model= ItemTipos
    template_name= TEMPL_ITEMTIPO_LIST
    fase_param = None
    
    def get_queryset(self):
        self.fase_param = Fase.objects.get(pk=self.kwargs['idfase'])
        return ItemTipos.objects.filter(idfase=self.fase_param)
    #Obtiene la fase para imprimir sus datos en el template  
    def get_context_data(self, **kwargs):
        context = super(ListaItemTipoView, self).get_context_data(**kwargs)
        context['fase'] = self.fase_param
        return context


class CreaItemTipoView(CreateView):
    """Crea un tipo de item """
    model= ItemTipos
    template_name = TEMPL_ITEMTIPFORM
    form_class = ItemTiposForm
    fase_param = None
    def get_success_url(self):
        return reverse('tipoitem_lista',kwargs={'idfase':self.kwargs['idfase']})
    def get_initial(self):
        fase = Fase.objects.get(pk=self.kwargs['idfase'])
        return { 'idfase': fase }


class EditaItemTipoView(UpdateView):
    """Edita un tipo de item"""
    model= ItemTipos
    template_name = TEMPL_ITEMTIPFORM
    form_class = ItemTiposForm
    def get_success_url(self):
        return reverse('tipoitem_lista',kwargs={'idfase':self.kwargs['idfase']})


class EliminarItemTipoView(DeleteView):
    model= ItemTipos
    #success_url = reverse_lazy('author-list')
    success_url = '/'


class CreaItemAtributoView(CreateView):
    """Crea un atributo en un tipo de item """
    model = ItemAtributos
    template_name = TEMPL_ATRIBUTOSFORM
    form_class = AtributosTiposForm
    def get_success_url(self):
        return reverse('itematributo_lista',kwargs={'idtipoitem':self.kwargs['idtipoitem']})
    def get_initial(self):
        itemtipo = ItemTipos.objects.get(pk=self.kwargs['idtipoitem'])
        return { 'idtipoitem': itemtipo }


class ListaItemAtributoView(ListView):
    """Lista los atributos de un tipo de item """
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
    