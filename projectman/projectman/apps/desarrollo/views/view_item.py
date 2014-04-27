from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projectman.apps.admin.models import  Fase
from ..models import Item
from ..forms import ItemForm, ItemFormN
from django.views.generic.edit import CreateView # , UpdateView, DeleteView
from view_oth import redirige_edicion_actual
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

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

