from django.views.generic import View  
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView 
from ...admin.models import Fase
from ..models import LineaBase
from ..models import SolicitudCambio
from ..forms import SolicitudCambioForm

class CreaSolicitudView(View):
    template_name = 'gestcambio/form_solicitudcambio.html'
    linea_base = None
    
    def get(self, request, idlinebase):
        
        form = self.crea_formulario(request, idlinebase)
        
        return render(request, self.template_name ,\
                       {'form': form, #'form_itemslb': form_itemslb ,\
                        'action': reverse('solicitud_crear', kwargs={'idlinebase': idlinebase}) })

    def post(self, request, *args, **kwargs):
        form = SolicitudCambioForm(request.POST)
        if form.is_valid():
            #guarda la cabecera y el detalle de la solicitud
            solicitud = form.save(commit=False)
            solicitud.save()
            form.save_m2m() # es necesarfio que el padre tenga commit=false 
            
        else:

            form = self.crea_formulario(request, self.kwargs['idlinebase'])
            return render(request, self.template_name, {'form': form ,'nodefault': '__panel.html'})
        
        linea_base = get_object_or_404(LineaBase, pk=int(self.kwargs['idlinebase']))
        
        return redirect(reverse('solicitudes_fase', \
                       kwargs={'idfase': linea_base.fase_id }))
        
    def crea_formulario(self, request, idlinebase):
        form = SolicitudCambioForm()
        #establece el solicitante por defecto 
        form.fields['solicitante'].initial = request.user
        
        linea_base = get_object_or_404(LineaBase, pk=idlinebase)
    
        #establece la linea base por defecto 
        form.fields['lineabase'].initial = linea_base
        #lista solo los items que pertenecen a la linea base 
        form.fields['items'].queryset = linea_base.items.all()
        
        return form


class ListaSolicitudesView(ListView):
    model = SolicitudCambio
    template_name = 'gestcambio/lista_solicitudes.html'
    
