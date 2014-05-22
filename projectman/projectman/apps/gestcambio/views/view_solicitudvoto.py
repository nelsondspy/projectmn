from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.db.models import Count
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
        return redirect( reverse('solicitudes_pend_proy',kwargs={'idproyecto':proyecto_id}))

    @classmethod
    def estado_votacion(self, idsolicitud ):
        """
        
        Metodo que determina el estado actual de la votacion para una solicitud.
        retorna una tupla de la siguiente estructura (votos a favor, votos en contra, votos faltantes )
        
        """
        votos_sol = SolicitudVoto.objects.filter(solicitud_id=idsolicitud)
        def prefvotos(x) : votos_sol.filter(aprobado=x).count()
        votos_favor = prefvotos(True)
        votos_contra = prefvotos(False)
        #obtenemos la cantidad de votos esperados que es  
        solicitud = get_object_or_404(SolicitudCambio, pk=idsolicitud)
        proyecto_id = solicitud.lineabase.fase.idproyecto_id
        (miembros, ) = CrearComiteProyectoView.miembros_proyecto(proyecto_id)
        vot_faltantes = miembros.count() - ( votos_favor + votos_contra )
        return (votos_favor, votos_contra, vot_faltantes)
    
