from django.views.generic import View  
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from ..models import LineaBase
from ...admin.models import Fase 
from django.views.generic import ListView 
from ..forms import SolicitudCambioForm

class CreaSolicitudView(View):
    template_name = 'gestcambio/form_solicitudcambio.html'
    
    def get(self, request, idlinebase):
        
        form = SolicitudCambioForm()
        line_base = get_object_or_404(LineaBase, pk=idlinebase)
        #lista solo los items que pertenecen a la linea base 
        form.fields['items'].queryset = line_base.items.all()
        return render(request, self.template_name ,\
                       {'form': form, #'form_itemslb': form_itemslb ,\
                        'action': reverse('solicitud_crear', kwargs={'idlinebase': idlinebase}) })
"""
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
            idfase = int(request.POST.get('fase',None))
            form.fields['items'].queryset = Item.objects.filter(idfase_id=idfase).\
                                                                exclude(estado=Item.E_BLOQUEADO).\
                                                                exclude(estado=Item.E_ELIMINADO)
            return render(request,TEMPL_FORM_LBITEM, {'form': form ,'nodefault': '__panel.html'})
        
        return redirect(reverse('lineabase_listar', \
                       kwargs={'idfase': self.kwargs['idfase']}))

"""