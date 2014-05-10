# -*- coding: utf-8 -*-
from django.views.generic import View  
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView 
from django.views.generic.edit import UpdateView
from django.contrib import messages

from ...desarrollo.models import Item
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
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        
        if self.kwargs.get('idsolicitud', None):
            context['idsolicitud'] = int(self.kwargs['idsolicitud'])
            
        if self.kwargs.get('idfase', None):
            context['idfase'] = self.kwargs['idfase']

        context['E_APROBADO'] = SolicitudCambio.E_APROBADO
        context['E_RECHAZADO'] = SolicitudCambio.E_RECHAZADO
        context['E_ENVIADO'] = SolicitudCambio.E_ENVIADO
        context['E_TERMINADO'] = SolicitudCambio.E_TERMINADO
        context['E_BORRADOR'] = SolicitudCambio.E_BORRADOR
        
        return  context



class SetSolicitudEnviada(View):
    template_name ='form_confirm_accion.html'

    def post(self, request, *args, **kwargs):
        """
        
        Establece el estado de la solicitud a enviada 
        
        """
        #establece el estado de la solicitud a enviada 
        solicitud_env = get_object_or_404(SolicitudCambio, pk=self.kwargs['pk'])
        solicitud_env.estado = SolicitudCambio.E_ENVIADO
        solicitud_env.save()
        messages.info(request, 'La solicitud fue enviada!')
        idfase = solicitud_env.lineabase.fase_id
        return redirect(reverse('solicitudes_fase', kwargs={'idfase' : idfase }))

    def get(self,request, pk ):
        """
        
        Despliega el formulario de confirmacion generico.
        Con valores particulares para confirmar el envio 
        
        """
        return render(request, self.template_name, {'action':reverse('solicitud_envia',\
                                                              kwargs={'pk':pk } ),\
                                             'titulo': 'Envio de solicitud',\
                                             'texto': '¿Está seguro que desea enviar?',\
                                             'value': 'Aceptar' })
        
class EditaSolicitudView(UpdateView):
    """
    
    Vista que permite modificar una solicitud de un item.
    El item debe encontrarse en estado borrador
    
    """
    template_name = 'gestcambio/form_solicitudcambio.html'
    form_class = SolicitudCambioForm
    model = SolicitudCambio
    
    def get_form(self, form_class):
        form = UpdateView.get_form(self, form_class)
        solicitud = get_object_or_404(SolicitudCambio, pk= self.kwargs['pk'] )
        
        form.fields['items'].queryset = solicitud.lineabase.items
        return form 
    
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('solicitud_edita', \
                                    kwargs={'pk':self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        
        return UpdateView.get_success_url(self)
