# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.generic.edit import CreateView  , UpdateView
from django.views.generic import ListView , View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.widgets import HiddenInput
#modelos 
from projectman.apps.admin.models import  Fase
from ..models import Item , ItemTipos
from ..models import ItemRelacion
#formularios
from ..forms import ItemForm, ItemFormN
from view_oth import redirige_edicion_actual
from view_oth import get_url_edicion_actual
#otros
from view_itemrelacion import CreaRelacionView

TEMPL_ITEMFORM = 'desarrollo/form_item.html'

@login_required
def procesa_item(request, accion=None,idelemento=None):
    if accion in ('editar', 'eliminar', 'crear'):
        if accion == 'eliminar':
            item = Item.objects.get(pk=idelemento) 
            item.delete()
            return redirige_edicion_actual(request, nivel=1)
        if accion =='editar' :
            item  = Item.objects.get(pk=idelemento) 
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
        if accion == 'crear':
            fase = Fase.objects.get(pk=idelemento) 
            item = Item(idfase=fase)
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
    if request.method == 'POST':
        #Edita una fase existente, o crear unan nueva
        idfasepost = request.POST.get('idfase',None)
        iditempost = request.POST.get('iditem',None)
        if iditempost:
            instancia_item = Item.objects.get(pk=iditempost)
        if idfasepost:
            fase = Fase.objects.get(pk=idfasepost)
            instancia_item = Item(idfase=fase)
            instancia_item.sigte_numero()
        itemform = ItemForm(request.POST, instance=instancia_item)
        if itemform.is_valid():
            itemform.save()     
            return redirige_edicion_actual(request, nivel=1)


class CreaItemView(CreateView):
    """
    
    Carga de datos basicos del Item 
    
    """
    model = Item
    form_class = ItemFormN
    template_name = 'desarrollo/form_item.html'
    fase_ob = None
    ocurrio_error = False

    def get_initial(self):
        
        self.fase_ob = get_object_or_404(Fase, pk=self.kwargs['idfase'])
        
        return { 'idfase': self.fase_ob } # es como hacer #form.idfase=fase
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['idfase'] = self.kwargs['idfase']
        context['action'] = reverse('item_crear', kwargs={'idfase': self.kwargs['idfase']})
        if self.ocurrio_error :
            context['nodefault'] = '__panel.html'
        return context
    
    def form_valid(self, form):
        form.instance.sigte_numero()
        return CreateView.form_valid(self, form)
    
    def form_invalid(self, form):
        self.ocurrio_error = True
        return CreateView.form_invalid(self, form)
    
    def get_success_url(self):
        idproyecto = self.fase_ob.idproyecto_id
        return reverse('expl_nivelfase',kwargs={'idproyecto':idproyecto , 
                                                'idfase' : self.kwargs['idfase'] })

    def get_form(self, form_class):
        form = CreateView.get_form(self, form_class)
        #obtiene solo los tipos de item que pertenecen a la fase 
        fase = get_object_or_404(Fase, pk=self.kwargs['idfase'])
        form.fields['idtipoitem'].queryset = ItemTipos.objects.filter(idfase=fase)
        return form


class SetEliminadoItemView(UpdateView):
    """
    
    Vista que permite cambiar es estado a un item a eliminado.
    Tambien establece como eliminado el estado de las relaciones que dependen del item.
    Si el item a eliminar es padre de alguna relacion se deniega el cambio de estado a eliminado
    
    """
    model = Item
    template_name = 'form_confirm_delete.html'
    
    def post(self, request, *args, **kwargs):
        #establece el estado de item  a eliminado
        
        item_eliminar = get_object_or_404(Item, pk=self.kwargs['pk'])
        item_eliminar.estado = Item.E_ELIMINADO
        item_eliminar.save()
        #establece el estado de las relaciones donde el item es hijo, a eliminadas
        #ya que el duenho de la relacion es el hijo 
        relaciones = ItemRelacion.objects.filter(destino=item_eliminar)
        for rel in relaciones: 
            rel.estado = ItemRelacion.E_ELIMINADO
            rel.save()
        
         
        return redirect(get_url_edicion_actual(request, nivel=1))

    def get_context_data(self, **kwargs):
        
        context = UpdateView.get_context_data(self, **kwargs)
        #ejecuta una serie de validaciones para permitir establecer a eliminado
        #o ocultar el formulario
        item_eliminar = get_object_or_404(Item, pk=self.kwargs['pk'])
        if not self.eliminacion_valida(item_eliminar):
            context['denegar_eliminacion'] = True

        context['action'] = reverse('item_eliminar' , kwargs={'pk':self.kwargs['pk']} )
        return context
    
    def eliminacion_valida(self, item):
        if self.item_espadre(item):
            messages.error(self.request, 'El item a eliminar es padre o antecesor de al menos un item' )
            return False
        return True

    def item_espadre(self, item):
        """
        devuelve true si el item es padre de otro
        
        """
        return ItemRelacion.objects.filter(origen=item).count() > 0


class EditItemView(UpdateView):
    """
    
    Modifica de datos basicos del Item.
    La modificacion del tipo de item no esta soportada.
    
    """
    model = Item
    form_class = ItemFormN
    template_name = 'desarrollo/form_item.html'
    fase_ob = None
    ocurrio_error = False

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['pk'] = self.kwargs['pk']
        context['action'] = reverse('item_editar', kwargs={'pk':self.kwargs['pk']})
        if self.ocurrio_error :
            context['nodefault'] = '__panel.html'
        return context
    
    def form_invalid(self, form):
        self.ocurrio_error = True
        return UpdateView.form_invalid(self, form)
    
    def get_success_url(self):
        return get_url_edicion_actual(self.request,nivel=1)

    def get_form(self, form_class):
        form = UpdateView.get_form(self, form_class)
        #por el momento no esta permitido el cambio de tipo de item
        form.fields['idtipoitem'].widget = HiddenInput()
        return form


class ListaEliminadosView(ListView):
    """ lista los items eliminados de una fase  """
    model = Item
    template_name = 'desarrollo/lista_itemseliminados.html'
    
    def get_queryset(self):
        """
        
        Lista los items en estado eliminado de una fase. 
        
        """
        object_list = Item.objects.filter(estado=Item.E_ELIMINADO).\
                        filter(idfase_id=self.kwargs['idfase'])
        return object_list


class RevivirItem(View):
    """
    
    Vista que establece el estado de los items de estado eliminado a activo.
    Ademas re-establece de nuevos las relaciones 
    
    """
    template_name ='form_confirm_accion.html'
    lista_errores = []
    items_rel_problemas=[]

    def post(self, request, *args, **kwargs):
        #establece el estado del item eliminado a desaprobado 
        item_arevivir = get_object_or_404(Item, pk=self.kwargs['pk'])
        item_arevivir.estado = Item.E_DESAPROBADO
        item_arevivir.save()
        #se activan las relaciones.Solo aquellas que no tienen conflictos
        #Lista relaciones eliminadas donde particpa el item , pero donde el item
        # no este relacionado con items eliminados 
        relac_items = ItemRelacion.objects.filter(Q(origen=item_arevivir) | \
                                                  Q(destino=item_arevivir)).\
                                                  exclude(origen__estado=ItemRelacion.E_ELIMINADO).\
                                                  exclude(destino__estado=ItemRelacion.E_ELIMINADO)
        for relacion in relac_items:
            
            #valida que la relacion no forme un ciclo
            if CreaRelacionView.valid_existe_ciclo(relacion.origen, relacion.destino):
                messages.error(request, 'se formara un ciclo ')
                #self.items_rel_problemas.append(relacion)
                continue #restringe que la relacion pueda tener un solo tipo de conflicto

            #valida que la relacion sea unica
            if CreaRelacionView.valid_relacion_unica(relacion.origen, relacion.destino):
                messages.error(request, 'la relacion ya existe ') 
                continue
            
            #valida que el antecesor este en  LB pero el sucesor si este en una LB
            if not CreaRelacionView.valid_ant_lineabase( relacion.origen, relacion.destino):
                messages.error(request, 'es necesario que el item antecesor tenga linea base ') 
                continue
            
            relacion.estado = ItemRelacion.E_ACTIVO
            relacion.save()

        messages.info(request, 'El item fue revivido!')
        
        #redirige a la lista de items eliminados
        return redirect(reverse('item_listaeliminados', kwargs={'idfase': item_arevivir.idfase_id }))

    def get(self,request, pk ):
        """
        
        Despliega el formulario de confirmacion generico.
        Con valores particulares para confirmar el envio 
        
        """
        return render(request, self.template_name, {'action':reverse('item_revivir',\
                                                              kwargs={'pk':pk } ),\
                                             'titulo': 'Revivir item',\
                                             'texto': '¿Está seguro que desea revivir este item?',\
                                             'value': 'Aceptar' })
