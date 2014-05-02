
from django.views.generic import View  
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from ..models import LineaBase
from ...admin.models import Fase 

from ..forms import LineaBaseForm
from ...desarrollo.models import Item

TEMPL_FORM_LBITEM = 'gestcambio/form_lineabase.html'

class CreaLineaBase(View):
    
    def get(self, request,idfase):
        fase_ob = get_object_or_404(Fase, pk=idfase)
        lineabase = LineaBase()
        lineabase.fase = fase_ob
        form = LineaBaseForm(instance=lineabase)
        #lista solo los items que pertenecen a la fase
        form.fields['items'].queryset = Item.objects.filter(idfase_id=idfase)
         
        return render(request,TEMPL_FORM_LBITEM,\
                       {'form': form, #'form_itemslb': form_itemslb ,\
                        'action': reverse('linea_base_item_crear', kwargs={'idfase': idfase}) })
    
    def post(self, request, *args, **kwargs):
        form = LineaBaseForm(request.POST)
        if form.is_valid():
            lineabase = form.save(commit=False)
            lineabase.save()
            form.save_m2m() # es necesarfio que el padre tenga commit=false  
        else:
            form = LineaBaseForm()
        #'action': reverse('linea_base_item_crear', kwargs={'idfase': sefl.kwargs[]}
        return render(request,TEMPL_FORM_LBITEM, {'form': form })
