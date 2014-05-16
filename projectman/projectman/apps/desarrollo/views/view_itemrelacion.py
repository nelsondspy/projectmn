
from django.views.generic.edit import CreateView,  DeleteView
from django.shortcuts import get_object_or_404 , redirect
from django.views.generic import ListView 
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages 
from django.db.models import Min

from ..models import ItemRelacion, Item 
from projectman.apps.admin.models import Fase

from ..forms import ItemRelacionForm

TEMPL_RELACION_FORM = 'desarrollo/form_relacion.html'
TEMPL_RELACION_LISTA = 'desarrollo/lista_relaciones.html'


class CreaRelacionView(CreateView):
    """
    
    Vista que permite crear relaciones entre items.
    De una misma fase.
    De fases antecesoras. 
    
    """
    model = ItemRelacion
    template_name = TEMPL_RELACION_FORM
    form_class = ItemRelacionForm
    valido = True
    
    
    def get_success_url(self):
        return reverse('relacion_listar', kwargs={'idproyecto':self.kwargs['idproyecto']})
    
    def get_form(self, form_class):
        form = CreateView.get_form(self, form_class)
        #el selector solo debe desplegar los items del proyecto 
        fases = Fase.objects.filter(idproyecto_id=self.kwargs['idproyecto'])
        #lista los items que coinciden con las fases de proyecto 
        items = Item.objects.filter(idfase__in=fases).exclude(estado=Item.E_ELIMINADO)
        #cargamos los selectores con los items y mostrando a que fase pertenecen 
        opciones = [(item.pk,'['+ item.idfase.__str__()[0:5]+'..] ' +\
                     '[' + item.estado +']  | ' +
                      item.nombre[0:40] ) for item in items]
        form.fields['origen'].choices = opciones
        form.fields['destino'].choices = opciones
        return form
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('relacion_crear',\
                                kwargs ={'idproyecto' :self.kwargs['idproyecto'] })
        if not self.valido:
            context['nodefault'] = '__panel.html'
            
        return context
    
    def form_valid(self, form):
        #establece el tipo de la relacion , si es interna a la fase o externa
        # es decir padre e hijo o antecesor sucesor.
        form.instance.set_tipo()
        relacion_str = form.instance.__str__()
        origen = form.instance.origen
        destino = form.instance.destino
        #Serie de validaciones 
        if self.valid_relacion_unica(origen, destino):
            messages.error(self.request, 'ERROR : La relacion ya existe: ' + relacion_str)
            self.valido = False
            return self.form_invalid(form)
        #valida la existencia de un ciclo
        if self.valid_existe_ciclo(form.instance.origen_id, form.instance.destino_id):
            messages.error(self.request, 'ERROR : Se ha detectado un ciclo: ' + relacion_str)
            self.valido = False
            return self.form_invalid(form)
        #valida que el antecesor este en linea base y el el hijo no tenga linea base si el hijo si 
        if not self.valid_ant_lineabase(origen, destino):
            messages.error(self.request,'ERROR : Si es una relacion interfase: \
            El item antecesor o padre debe estar en linea.Si es una relacion intra-fase:\
            El item hijo no debe tener linea base. ')
            self.valido = False
            return self.form_invalid(form)
        #
        if not self.valid_intra_fase_bloq(origen, destino):
            messages.error(self.request,'ERROR : Si es una relacion intrafase y ambos items \
            ya estan en linea base entonces la relacion ya no esta permitida. \
            En estado desarrollo debe establecer las relaciones')
            self.valido = False
            return self.form_invalid(form)

        
        messages.info(self.request, 'Relacion creada : ' + relacion_str)
        return CreateView.form_valid(self, form)
    
    def form_invalid(self, form):
        self.valido = False
        return CreateView.form_invalid(self, form)
    
    @classmethod
    def __lista_antecesores(self,idItem):
        #retorno = list(db.session.query(Relacion).filter(Relacion.idSucesor == idItem ).all())
        retorno = ItemRelacion.objects.filter(destino_id=idItem)
        antecesores = []
        for r in retorno:
            antecesores.append(r.origen_id)
            antecesores += self.__lista_antecesores(r.origen_id)
        return antecesores

    @classmethod
    def __lista_sucesores(self,idItem):
        #retorno = list(db.session.query(Relacion).filter(Relacion.idAntecesor == idItem ).all())
        retorno = ItemRelacion.objects.filter(origen_id=idItem)
        sucesores = []
        for r in retorno:
            sucesores.append(r.destino_id)
            sucesores += self.__lista_sucesores(r.destino_id)
        return sucesores

    @classmethod
    def valid_existe_ciclo(self, idorigen, iddestino):
        """
        
        Destecta un ciclo en un par de items (origen , destino).
        
        Se carga listas todos los de origenes posibles y destinos posibles
        Se itera para verificar si existe alguna forma de llegar 
        al origen por medio del destino
        Retorna True si existe el camino. 
        
        """
        # caso autociclo
        if idorigen == iddestino:
            return True
        a = self.__lista_antecesores(idorigen)
        b = self.__lista_sucesores(iddestino)
        # caso sencillo 1->2, 2->1
        for ante in a:
            if str(ante) == str(iddestino):
                return True
        #otros casos
        for isgte in a:
            for iant in b:
                if( isgte == iant):
                    return True
        
        return False 
    
    @classmethod
    def valid_relacion_unica(self,porigen, pdestino):
        """
    
        Valida que aun no exista la relacion.
        -Tiene en cuenta que pueden existir relaciones eliminadas y las ignora.
    
        """
        relacion = ItemRelacion.objects.filter(Q(origen=porigen) & Q(destino=pdestino)).\
        exclude(estado=ItemRelacion.E_ELIMINADO)
        return relacion.count()
    
    @classmethod
    def valid_ant_lineabase(self, porigen, pdestino):
        """
        
        Valida relaciones entre items con respecto a que existencia alguna linea base. 
        Si el item padre no tiene linea base el hijo o antecesor tampoco debe tener linea base.
        
        """
        if porigen.estado == Item.E_BLOQUEADO :
            return True
        #si es una relacion interfase
        if porigen.idfase_id != pdestino.idfase_id:
            if porigen.estado != Item.E_BLOQUEADO:
                return False #porque el antecesor debe estar bloqueado
        else: #es una relacion intra-fase 
            if pdestino.estado == Item.E_BLOQUEADO :
                return False 
        return True
    
    @classmethod
    def valid_intra_fase_bloq(self, porigen, pdestino):
        """
        
        Valida que la relacion no se produzca entre items bloqueados de la misma fase.
        porque estos items al estar bajo una linea base tambien se deben evitar nuevas relaciones entre ellas 
        
        """
        #son de la misma fase 
        if porigen.idfase_id == pdestino.idfase_id:
            #el origen esta bloqueado
            if porigen.estado == Item.E_BLOQUEADO :
                #el destino tambien esta bloqueado
                if pdestino.estado == Item.E_BLOQUEADO :
                    return False #no es posible esta relacion
                
        return True



class ListaRelacionesView(ListView):
    """
    
    Vista que consulta las relaciones a nivel de :
    -Fase.
    -Item.
    -Proyecto en general.
    
    """
    model = ItemRelacion
    template_name = TEMPL_RELACION_LISTA
    
    def get_queryset(self):
        
        #lista las relaciones que tiene una fase 
        if self.kwargs.get('idfase',None):
            object_list = None
        
        #lista todas las relaciones que implican ese item
        if self.kwargs.get('iditem',None):
            object_list = ItemRelacion.objects.filter().all()
            
        #lista todas las relaciones que implican ese item
        if self.kwargs.get('idproyecto',None):
            #No es optima esta consulta
            fases = Fase.objects.filter(idproyecto_id=self.kwargs.get('idproyecto'))
            items = Item.objects.filter(idfase__in=fases)
            
            object_list = ItemRelacion.objects.filter((Q(origen__in=items)|\
                                                       Q(destino__in=items)) &\
                                                    Q(estado=ItemRelacion.E_ACTIVO))
        return object_list
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['idproyecto'] = self.kwargs.get('idproyecto')
        return context 


class EliminaRelacionView(DeleteView):
    """
    
    Permite eliminar una relacion
    
    """
    model = ItemRelacion
    template_name = 'form_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('relacion_eliminar',\
                                    kwargs = {'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']
    
    def delete(self, request, *args, **kwargs):
        relacion = self.get_object()
        (validez, mensaje) = self.valid_eliminar_rel(relacion)
        if validez:
            messages.success(request,mensaje)
            
            return DeleteView.delete(self, request, *args, **kwargs)
            
        else:
            messages.error(request,'ERROR : '+ mensaje)
            return redirect(self.get_success_url())

        return DeleteView.delete(self, request, *args, **kwargs)

    @classmethod
    def valid_eliminar_rel(self, relacion):
        if relacion.origen.estado == Item.E_BLOQUEADO :
            if relacion.destino.estado == Item.E_BLOQUEADO:
                return (False, 'No es posible eliminar la relacion entre items con linea base')

        return (True, 'Relacion Eliminada')


def valid_item_eshuerfano(iditem):
    """
    
    Metodo que determina si un item es huerfano.
    -Se dice que un item es huerfano si ningun item tiene \
     relacion de antecesor o padre con este item.
    -Retorna true si el item es huerfano.
    """
    #items sin relaciones 
    return not (ItemRelacion.objects.filter(destino_id=iditem).\
                exclude(estado=ItemRelacion.E_ELIMINADO).count() > 0 )
    
def lista_huerfanos_fase(fase_id):
    """
    Funcion que devuelve un queryset de los items en una fase \
    que cumplen las siguientes condiciones:
    - los items no estan eliminados 
    
    
    """
    #obtiene la primera fase del proyecto (la que tiene menor id)
    min_fase = Fase.objects.aggregate(min_fase=Min('idfase')).get('min_fase')
    qs_fase = Item.objects.filter(idfase_id=min_fase).\
            exclude(estado=Item.E_ELIMINADO)
    #obtiene el primer item de la fase (el que tiene menor id)
    min_item = qs_fase.aggregate(min_item=Min('iditem')).get('min_item')
    
    qs_relaciones_fase = ItemRelacion.objects.\
            filter(destino__idfase_id=fase_id).values('destino')

    #exclude los items eliminados y el primer item de la primera fase 
    qs_items_huerfanos = Item.objects.filter(idfase_id=fase_id).exclude(estado=Item.E_ELIMINADO)\
        .exclude(iditem__in=qs_relaciones_fase).exclude(pk=min_item)
        
    return qs_items_huerfanos

    
