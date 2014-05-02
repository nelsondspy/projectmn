
from django.views.generic import View  
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from ..models import LineaBase
from ...admin.models import Fase 
from django.views.generic import ListView 
    

from ..forms import LineaBaseForm
from ...desarrollo.models import Item

TEMPL_FORM_LBITEM = 'gestcambio/form_lineabase.html'

class CreaLineaBase(View):
    
    def get(self, request, idfase):
        fase_ob = get_object_or_404(Fase, pk=idfase)
        lineabase = LineaBase()
        lineabase.fase = fase_ob
        form = LineaBaseForm(instance=lineabase)
        #lista solo los items que pertenecen a la fase
        form.fields['items'].queryset = Item.objects.filter(idfase_id=idfase).\
            exclude(estado=Item.E_BLOQUEADO)
        return render(request,TEMPL_FORM_LBITEM,\
                       {'form': form, #'form_itemslb': form_itemslb ,\
                        'action': reverse('linea_base_item_crear', kwargs={'idfase': idfase}) })
    
    def post(self, request, *args, **kwargs):
        form = LineaBaseForm(request.POST)
        if form.is_valid():
            #guarda la cabecera y el detalle de la linea base
            lineabase = form.save(commit=False)
            lineabase.save()
            form.save_m2m() # es necesarfio que el padre tenga commit=false 
            
            lineabase_pers = LineaBase.objects.get(pk=lineabase.pk)
            items = lineabase_pers.items.all()
            
            #establece el estado de los items selecionados en la lb a bloqueado
            for item in items:
                item.estado = Item.E_BLOQUEADO
                item.save()
        else:
            form = LineaBaseForm()
            return render(request,TEMPL_FORM_LBITEM, {'form': form })
        
        return redirect(reverse('lineabase_listar', \
                       kwargs={'idfase': self.kwargs['idfase']}))


class ListarLineaBaseView(ListView):
    """
    Despliega una lista de LineasBase del sistema.
    
    """
    model= LineaBase
    template_name = 'gestcambio/lista_lineabase.html'
    lista_items = None

    def get_queryset(self):
        #lista solo las lineas bases de la fase 
        object_list = LineaBase.objects.filter(fase_id=self.kwargs['idfase'])
        if self.kwargs.get('idlineabase', None):
            
            lineabase = get_object_or_404(LineaBase,pk=self.kwargs['idlineabase'])
            self.lista_items = lineabase.items.all()
            
        
        return object_list
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['idfase'] = self.kwargs['idfase']
        if self.kwargs.get('idlineabase', None):
            context['idlineabase'] = int(self.kwargs['idlineabase'])
        context['itemslb'] = self.lista_items
        return context