from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.db import transaction
from django.contrib import messages
from ..models import SolicitudCambio, SolicitudVoto, ComiteProyecto
from django.db.models import Q
from django.http import Http404

from view_comite import  CrearComiteProyectoView
class ListaSolicPendientes(ListView):
    
    template_name = 'gestcambio/lista_solic_pendientes.html'
    #lista de solicitudes, no votadas en el proyecto 
    # la solicitud debe ur dirigida al comite
    # el usuario debe formar parte del comite
    
    def get_queryset(self):
        proyecto_id = self.kwargs['idproyecto']
        
        miembro = ComiteProyecto.objects.filter(usuario=self.request.user).\
            filter(proyecto=proyecto_id)
        if miembro.count()< 1 :
            messages.info(self.request, 'Usted no es miembro del comite de este proyecto ' )
            return []
        
        solic_votadas = SolicitudVoto.objects.filter(Q(miembro__usuario=self.request.user)\
                                   & Q(miembro__proyecto_id=proyecto_id)).values('solicitud_id')
        
        object_list = SolicitudCambio.objects.filter(lineabase__fase__idproyecto_id=proyecto_id).\
            filter(estado=SolicitudCambio.E_ENVIADO).\
            exclude(pk__in=solic_votadas)
        return object_list
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['idproyecto'] = self.kwargs['idproyecto']
        context['E_APROBADO'] = SolicitudCambio.E_APROBADO
        context['E_RECHAZADO'] = SolicitudCambio.E_RECHAZADO
        context['E_ENVIADO'] = SolicitudCambio.E_ENVIADO
        context['E_TERMINADO'] = SolicitudCambio.E_TERMINADO
        context['E_BORRADOR'] = SolicitudCambio.E_BORRADOR
        

        return context

class VotaSolicitudView(View):
    template_name ='form_confirm_accion.html'
    APROBAR ='aprobar'
    RECHAZAR = 'rechazar'
    ACCIONES_POSIBLES = (APROBAR, RECHAZAR)

    def get(self,request,accion, pk ):
        """

        Despliega el formulario de confirmacion generico.
        Con valores particulares para confirmar el voto de aprobacion o el rechazo de
        una solicitud de cambio.

        """
        if not accion in self.ACCIONES_POSIBLES:
            raise Http404
        
        get_object_or_404(SolicitudCambio, pk=pk)
        
        if accion == self.APROBAR:
            mensaje = 'Esta seguro que desea APROBAR la solicitud de cambio?'
        else:
            mensaje = 'Esta seguro que desea RECHAZAR la solicitud de cambio?'
            
        return render(request, self.template_name, {'action':reverse('solicitud_votar',\
                                                              kwargs={'pk':pk, 'accion':accion } ),\
                                             'titulo': 'Voto de solicitud',\
                                             'texto': mensaje ,\
                                             'value': 'Aceptar' })
    @transaction.atomic
    def post(self,request, *args, **kwargs):
        """
        Guarda el nuevo voto.
        
        """
        accion = self.kwargs['accion']
        pk = self.kwargs['pk']
        if not accion in self.ACCIONES_POSIBLES:
            raise Http404
        
        solicitud = get_object_or_404(SolicitudCambio, pk=pk)
        proyecto_id = solicitud.lineabase.fase.idproyecto_id
        miembro = get_object_or_404(ComiteProyecto, proyecto_id=proyecto_id, usuario=request.user )
        #nueva instancia de voto
        voto = SolicitudVoto()
        voto.solicitud=solicitud
        voto.miembro=miembro
        voto.aprobado = (accion==self.APROBAR) 
        voto.save()
        messages.success(request,'Voto enviado exitosamente')
        #una vez registrado el voto del usuario determina si la solicitud fue aprobada
            #o rechazada , si la cant de votos faltantes es 0 entonces 
            #se aprueba o rechaza la solicitud
        (favor, contra, faltantes ) = self.estado_votacion(solicitud.pk)
        if faltantes == 0 :
            if favor > contra:
                solicitud.estado = SolicitudCambio.E_APROBADO
                messages.success(request,'La solicitud fue APROBADA')
            else:
                solicitud.estado = SolicitudCambio.E_RECHAZADO
                messages.warning(request,'La solicitud fue RECHAZADA')
            #
            solicitud.save()
        
        
        return redirect( reverse('solicitudes_pend_proy',kwargs={'idproyecto':proyecto_id}))

    @classmethod
    def estado_votacion(self, idsolicitud ):
        """
        
        Metodo que determina el estado actual de la votacion para una solicitud.
        retorna una tupla de la siguiente estructura (votos a favor, votos en contra, votos faltantes )
        
        """
        votos_sol = SolicitudVoto.objects.filter(solicitud_id=idsolicitud)
        votos_favor = votos_sol.filter(aprobado=True).count()
        votos_contra = votos_sol.filter(aprobado=False).count()
        #obtenemos la cantidad de votos esperados que es  
        solicitud = get_object_or_404(SolicitudCambio, pk=idsolicitud)
        proyecto_id = solicitud.lineabase.fase.idproyecto_id
        (miembros, validez, msg ) = CrearComiteProyectoView.miembros_proyecto(proyecto_id)
        vot_faltantes = miembros.count() - ( votos_favor + votos_contra )
        return (votos_favor, votos_contra, vot_faltantes)
    

class EstadoVotacionView(ListView):
    """
    
    Vista que muestra el estado de la votacion
    
    """
    model = SolicitudVoto
    template_name = 'gestcambio/lista_estadovotacion.html'
    
    def get_queryset(self):
        idsolicitud = self.kwargs['idsolicitud']
        votos_sol = SolicitudVoto.objects.filter(solicitud_id=idsolicitud)
        return votos_sol


    def get_context_data(self, **kwargs):
        idsolicitud = self.kwargs['idsolicitud']
        context = ListView.get_context_data(self, **kwargs)
        estado = VotaSolicitudView.estado_votacion(idsolicitud)
        context['favor'] = estado[0]
        context['contra'] = estado[1]
        context['faltantes'] = estado[2]
        return context