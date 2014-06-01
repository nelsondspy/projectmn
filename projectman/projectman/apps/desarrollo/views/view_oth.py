from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projectman.apps.admin.models import  Proyecto, Fase
from ..models import  Item, ItemRelacion
from ...gestcambio.models import  SolicitudCambio

#nombres de variables de sesion 
SESS_IDPROYECTO = 'idproyecto'
SESS_IDFASE = 'idfase'


#nombres de templates 
TEMPL_PANEL = '__panel.html'
TEMPL_EXPLORADOR = 'explorador_comp.html'


@login_required
def mostrar_panel(request):
    return render(request, TEMPL_PANEL)



def redirige_edicion_actual(request, nivel=0):
    """
    
    Redirige a la vista que muestra el proyecto/fase/item que se esta editando
    actualmente, segun las variables de sesion, por niveles de url 
    
    """
    #por defecto el nivel 0 es el proyecto
    url_redirigir = '/desarrollo/componentes/'+ request.session[SESS_IDPROYECTO]
    #el nivel 1 es la fase
    if nivel == 1: 
        url_redirigir  += '/'+request.session[SESS_IDFASE]
    #el nivel 2 es el item 
    return redirect(url_redirigir)


def get_url_edicion_actual(request, nivel=0):
    """
    
    Retorna la url que corresponde de la edicion actual del proyecto.
    Utiliza la variables de sesion para determinar el proyecto con el cual esta trabajando
    
    """
    #Utiliza las variables de sesion cargadas en la navegacion
    #para redireccionar al proyecto y la fase.  
    idproyecto = int(request.session[SESS_IDPROYECTO])
    
    
    if nivel == 0:
        return reverse('editor_componentes',kwargs={'idproyecto': idproyecto })

    if nivel == 1:
        idfase = int(request.session[SESS_IDFASE])
        return reverse('expl_nivelfase',kwargs={'idproyecto': idproyecto , 
                                                'idfase' : idfase})


@login_required
def editor_componentes(request, idproyecto=None, idfase=None):
    """"
    
    Explorador de componentes de forma jerarquica permite:
    -Listar fases, 
    -Los items de una fase
    -indica que item posee alguna solicitud de cambio sin ejecutar
    
    Envia los valores de las constantes de estado para la impresion de iconografia.
    
    """

    proyecto = Proyecto.objects.get(pk=idproyecto)
    request.session[SESS_IDPROYECTO] = idproyecto
    request.session[SESS_IDFASE] = None
    #lista las fases del proyecto  
    lista_fases = Fase.objects.order_by('idfase').filter(idproyecto=idproyecto)
    #lista de items de una fase seleccionada ( recibida como parametro) 
    # cuyo estado no sea eliminado 
    items_afectados = None
    lista_items = None
    if idfase:
        request.session[SESS_IDFASE] = idfase
        lista_items = Item.objects.order_by('numero').\
            filter(idfase=idfase).exclude(estado=Item.E_ELIMINADO )
        
        #lista las solicitudes de cambio para mostrar en el panel los items que requieren atencion
        lista_solic = SolicitudCambio.objects.filter(solicitante=request.user).\
                filter(estado=SolicitudCambio.E_APROBADO).\
                filter(lineabase__fase__idfase=idfase)
        
        #crea un  array de items afectados por las solicitudes
        lc_items =  [solic.items.all().values('iditem') for solic in lista_solic]
        if len(lc_items)>0 :
            items_afectados = []
            for sub_iditem in lc_items[0]:
                items_afectados.append(sub_iditem['iditem'])
        
        idfase = int(idfase) # en la plantilla se requier el valor entero no el unicode

    #valores constantes de estado para las fase
    estados_fase = {'E_DESARROLLO':Fase.E_DESARROLLO, 'E_FINALIZADO': Fase.E_FINALIZADO}
    estados_item = {'E_BLOQUEADO': Item.E_BLOQUEADO, 'E_DESAPROBADO':Item.E_DESAPROBADO,\
                     'E_REVISION' : Item.E_REVISION}
    return render(request , TEMPL_EXPLORADOR , {'proyecto': proyecto , 'idfase':idfase,
                    'lista_fases':lista_fases ,\
                     'lista_items':lista_items, 'I_BLOQ':Item.E_BLOQUEADO,\
                     'EST_FASE':  estados_fase, 'EST_ITEM': estados_item,\
                     'items_afectados': items_afectados })


class GraficoProyecto(ListView):
    """
    
    """
    template_name='projectmn_drw.html'
    

    def get_queryset(self):
        lista_fases = []
        idproyecto = self.kwargs['idproyecto']
        lista_fases_qs = Fase.objects.order_by('idfase').\
            filter(idproyecto=idproyecto)
        for fase in lista_fases_qs:
            lista_fases.append({'pk':fase.idfase, 'nombre':fase.nombre,\
                                 'items':Item.objects.filter(idfase=fase).\
                                 exclude(estado=Item.E_ELIMINADO)})
        
        relaciones = ItemRelacion.objects.filter(Q(origen__idfase__idproyecto=idproyecto) |\
                                                 Q(destino__idfase__idproyecto=idproyecto))
        
        nombre_proyecto = lista_fases_qs[0].idproyecto if lista_fases_qs.count()>0 else ''

        lista_objetos={'fases':lista_fases, 'relaciones':relaciones, 'proyecto': nombre_proyecto}
        
        return lista_objetos
    
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context