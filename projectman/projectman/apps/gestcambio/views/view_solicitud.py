# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.db import transaction
from django.contrib import messages

from view_comite import  CrearComiteProyectoView
from ..models import LineaBase
from ..models import SolicitudCambio
from ..forms import SolicitudCambioForm
from ...desarrollo.models import Item, ItemAtributosValores
from ...admin.models  import Fase

class CreaSolicitudView(View):
    template_name = 'gestcambio/form_solicitudcambio.html'
    linea_base = None
    comite_miembros = None

    def get(self, request, idlinebase):
        (validez, msg )= self.validaciones(idlinebase)
        if not validez:
            #messages.error(request, msg)
            return render(request, 'form_confirm_accion.html', {'action': request.META['HTTP_REFERER'] ,\
                                             'titulo': 'ADVERTENCIA',\
                                             'texto': msg ,\
                                             'value': '' })

            

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

            formred = self.crea_formulario(request, self.kwargs['idlinebase'], form)
            return render(request, self.template_name, {'form': formred ,'nodefault': '__panel.html'})

        linea_base = get_object_or_404(LineaBase, pk=int(self.kwargs['idlinebase']))

        return redirect(reverse('solicitudes_proyecto', \
                       kwargs={'idproyecto': linea_base.fase.idproyecto_id }))

    def crea_formulario(self, request, idlinebase , instance=None):
        if not instance:
            form = SolicitudCambioForm()
        else:
            form = instance
        #establece el solicitante por defecto
        form.fields['solicitante'].initial = request.user

        linea_base = get_object_or_404(LineaBase, pk=idlinebase)

        #establece la linea base por defecto
        form.fields['lineabase'].initial = linea_base
        #lista solo los items que pertenecen a la linea base
        form.fields['items'].queryset = linea_base.items.all()

        return form
    
    def validaciones(self, idlinebase):
        #valida la cantidad de miembros
        proyecto_id = LineaBase.objects.get(pk=idlinebase).fase.idproyecto_id
        (miembros, valido, mensaje) = CrearComiteProyectoView.miembros_proyecto(proyecto_id)
        
        self.comite_miembros = miembros
        
        if not valido:
            return (valido, mensaje)
        
        #valida que la fase se encuentre en estado de desarrollo 
        if LineaBase.objects.get(pk=idlinebase).fase.estado != Fase.E_DESARROLLO :
            return (False, 'La fase ya se encuentra finalizada, no puede realizar modificaciones ')
        
        return (True, '')
        
 
class ListaSolicitudesView(ListView):
    model = SolicitudCambio
    template_name = 'gestcambio/lista_solicitudes.html'
    titulo = ''
    explicacion = ''
    usuario_essolic = False

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)

        if self.kwargs.get('idsolicitud', None):
            context['idsolicitud'] = int(self.kwargs['idsolicitud'])

        if self.kwargs.get('idfase', None):
            context['idfase'] = self.kwargs['idfase']
        #solicitudes_proyecto
        if self.kwargs.get('idproyecto', None):
            context['idproyecto'] = self.kwargs['idproyecto']
        
        EST_SOLICITUD = {'E_APROBADO': SolicitudCambio.E_APROBADO, \
                         'E_RECHAZADO': SolicitudCambio.E_RECHAZADO,\
                         'E_ENVIADO': SolicitudCambio.E_ENVIADO, \
                         'E_TERMINADO': SolicitudCambio.E_TERMINADO,\
                         'E_BORRADOR': SolicitudCambio.E_BORRADOR }
        #variable que indica si el usuario es miembro del comite
        if self.usuario_essolic:
            context['usuario_essolic'] = self.usuario_essolic
            
        context['EST_SOLICITUD'] = EST_SOLICITUD
        context['titulo'] = self.titulo 
        context['explicacion'] = self.explicacion 

        return  context
    def get_queryset(self):
        #solicitudes_proyecto
        if self.kwargs.get('idproyecto', None) and not self.kwargs.get('propios', None):
            #solicitud.lineabase.fase
            idproyecto = self.kwargs.get('idproyecto', None)
            object_list = SolicitudCambio.objects.filter(lineabase__fase__idproyecto_id=idproyecto).\
                exclude(estado=SolicitudCambio.E_BORRADOR)
            self.titulo = 'Solicitudes de cambio en el proyecto'
            self.explicacion = 'Todas las solicitudes enviadas ,aprobadas y rechazadas en el proyecto'

        #solicitudes_del proyecto que hechas por el usuario
        if self.kwargs.get('idproyecto', None) and self.kwargs.get('missolicitudes', None):
            idproyecto = self.kwargs.get('idproyecto', None)
            object_list = SolicitudCambio.objects.filter(lineabase__fase__idproyecto_id=idproyecto).\
                filter(solicitante=self.request.user)
            
            #indica si el usuario fue el que hizo la solicitud y permite ocultar opciones 
            if object_list.count()> 0:
                self.usuario_essolic = object_list[0].solicitante == self.request.user
            
            self.titulo = 'Mis solicitudes de cambio'
            self.explicacion = 'Todas las solicitudes creadas por mi (aprobadas, rechazadas , enviadas y  en borrador) '

        return object_list


class SetSolicitudEnviada(View):
    template_name ='form_confirm_accion.html'
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """

        Establece el estado de la solicitud a enviada

        """
        #establece el estado de la solicitud a enviada
        solicitud_env = get_object_or_404(SolicitudCambio, pk=self.kwargs['pk'])
        solicitud_env.estado = SolicitudCambio.E_ENVIADO
        solicitud_env.save()
        messages.info(request, 'La solicitud fue enviada!')
        idproyecto = solicitud_env.lineabase.fase.idproyecto_id
        return redirect(reverse('solicitudes_proyecto', kwargs={'idproyecto' : idproyecto }))

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
        pk = self.kwargs['pk']
        solicitud = get_object_or_404( SolicitudCambio, pk= pk)
        return reverse('solicitudes_proyecto', \
            kwargs={'idproyecto': solicitud.lineabase.fase.idproyecto_id })


class EliminaSolicitudView(DeleteView):
    """

    Solicita confirmacion para eliminar una solicitud de cambio

    """
    model = SolicitudCambio
    template_name = 'form_confirm_delete.html'

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('solicitud_eliminar', kwargs={'pk':self.kwargs['pk']})
        return context
    
class DetalleSolicitud(DetailView):
    context_object_name = "solicitud"
    model = SolicitudCambio
    template_name = 'gestcambio/detalle_solicitudcambio.html'


class SetSolicitudEjecutada(View):
    """
    
    Vista que permite establecer el estado de una solicitud de aprobada a terminada.
    Muestra un mensaje solicitando confirmacion.
    Si el usuario acepta envia una peticion post y realizar el cambio de estado. 
    
    """
    template_name ='form_confirm_accion.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """

        Establece el estado de la solicitud a aprobada

        """
        #establece el estado de la solicitud a enviada
        solicitud_aprob = get_object_or_404(SolicitudCambio, pk=self.kwargs['pk'])
        solicitud_aprob.estado = SolicitudCambio.E_TERMINADO
        solicitud_aprob.save()
        messages.success(request, 'La solicitud fue terminada')

        #se debe reestablecer el estado de los items afectados a bloqueado
        lista_items = solicitud_aprob.items.all()
        for item in lista_items:
            item.estado = Item.E_BLOQUEADO
            item.save()
            #valores actuales del item, afectados por la linea base 
            valores = ItemAtributosValores.objects.filter(iditem=item).\
                filter(usoactual=True)
            #establece como true el indicador 
                #que el valor se encuentra bajo linea base
            for val_act in valores:
                val_act.enlineabase =  True
                val_act.save()

        #redirecciona a la lista de solicitudes del usuario
        idproyecto = solicitud_aprob.lineabase.fase.idproyecto_id
        return redirect(reverse('solicitudes_usuario', kwargs={'idproyecto' : idproyecto,\
                                                                'missolicitudes': 1}))

    def get(self,request, pk ):
        """

        Despliega el formulario de confirmacion generico.
        Con valores particulares para confirmar la terminacion de la solicitud.

        """
        confirm = {'action':reverse('solicitud_terminar',kwargs={'pk':pk } ),\
                    'titulo': 'Terminar la solicitud',\
                    'texto': '¿Está seguro que desea terminar la ejecucion de la solicitud ?',\
                    'value': 'Aceptar' }
        
        return render(request, self.template_name, confirm)

