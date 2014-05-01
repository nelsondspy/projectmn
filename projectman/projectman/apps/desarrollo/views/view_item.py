from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView  , UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
#modelos 
from projectman.apps.admin.models import  Fase
from ..models import Item , ItemTipos
#formularios
from ..forms import ItemForm, ItemFormN
from view_oth import redirige_edicion_actual
from view_oth import SESS_IDFASE, SESS_IDPROYECTO 
from twisted.python.hook import POST


TEMPL_ITEMFORM = 'desarrollo/'

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


class CreaItemView(CreateView):
    """
    
    Carga de datos basicos del Item 
    
    """
    model = Item
    form_class = ItemFormN
    template_name = 'desarrollo/form_item.html'
    fase_ob = None
    ocurrio_error = False

    def get_initial(self):
        
        self.fase_ob = get_object_or_404(Fase, pk=self.kwargs['idfase'])
        
        return { 'idfase': self.fase_ob } # es como hacer #form.idfase=fase
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['idfase'] = self.kwargs['idfase']
        if self.ocurrio_error :
            context['nodefault'] = '__panel.html'
        return context
    
    def form_valid(self, form):
        form.instance.sigte_numero()
        return CreateView.form_valid(self, form)
    
    def form_invalid(self, form):
        self.ocurrio_error = True
        return CreateView.form_invalid(self, form)
    
    def get_success_url(self):
        idproyecto = self.fase_ob.idproyecto_id
        return reverse('expl_nivelfase',kwargs={'idproyecto':idproyecto , 
                                                'idfase' : self.kwargs['idfase'] })

    def get_form(self, form_class):
        form = CreateView.get_form(self, form_class)
        #obtiene solo los tipos de item que pertenecen a la fase 
        fase = get_object_or_404(Fase, pk=self.kwargs['idfase'])
        form.fields['idtipoitem'].queryset = ItemTipos.objects.filter(idfase=fase)
        return form


class SetEliminadoItemView(UpdateView):
    """
    
    Vista que permite cambiar es estado a un item a eliminado.
    
    """
    model = Item
    template_name = 'form_confirm_delete.html'
    
    
    def post(self, request, *args, **kwargs):
        #establece el estado de item  a eliminado
        item_eliminar = get_object_or_404(Item, pk=self.kwargs['pk'])
        item_eliminar.estado = Item.E_ELIMINADO
        item_eliminar.save()
        
        #Utiliza las variables de sesion cargadas en la navegacion
        #para redireccionar al proyecto y la fase.  
        idproyecto = int(self.request.session[SESS_IDPROYECTO])
        idfase = int(self.request.session[SESS_IDFASE])
 
        return redirect (reverse('expl_nivelfase',kwargs={'idproyecto':idproyecto , 
                                                'idfase' : idfase}))

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('item_eliminar' , kwargs={'pk':self.kwargs['pk']} )
        return context
