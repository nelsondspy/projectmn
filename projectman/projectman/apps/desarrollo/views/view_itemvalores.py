from django.views.generic import View , ListView

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db import transaction
from django.contrib import messages 

from ..models import ItemAtributosValores
from ..models import ItemTipos
from ..models import ItemAtributos
from ..forms import ItemValoresForm
from ..models import Item
from view_oth import get_url_edicion_actual 


TEMPL_FORMASIG='desarrollo/form_itemvaloresatributos.html'


class AsignaValoresItem(View):
    """
    
    Vista que permite asignar valores a los items.
    Crea los valores con valores por defecto , segun el tipo de dato
    del atributo
    
    """
    
    ValoresFormSet = modelformset_factory(model=ItemAtributosValores, form=ItemValoresForm,extra=0)

    def get(self, request,iditem):
        item = get_object_or_404(Item, pk=iditem)
        #si no existe valor alguno instancia los atributos del supertipo
        tipo_default = ItemTipos.objects.filter(es_supertipo=True)
        tipo_item = ItemTipos.objects.filter(pk=item.idtipoitem_id)
        #consulta todos los atributos comunes y los del tipo  de item 
        atributos = ItemAtributos.objects.filter(Q(idtipoitem=tipo_default) |\
                                                          Q(idtipoitem=tipo_item))
        for atrr in atributos:
            existe = ItemAtributosValores.objects.filter(idatributo = atrr,\
                                                 iditem = item, usoactual = True)
            if existe.count() == 0:
                
                atributovalor = ItemAtributosValores(idatributo = atrr,\
                                                 iditem = item,usoactual = True)
                atributovalor.set_valor_default()
                atributovalor.save()
        #pos insercion la lista de atributos con valores intanciados  del item
        lista_valores = ItemAtributosValores.objects.filter(iditem=item).exclude(usoactual=False)
        formset = self.ValoresFormSet(queryset=lista_valores)
        #return render_to_response(TEMPL_FORMASIG,{'formset': formset})
        
        return render(request, TEMPL_FORMASIG, {'formset': formset, \
                                                'action': reverse('valores_asignar',\
                                                                  kwargs={'iditem':iditem} ) 
                                                })
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        
        Metodo transaccional que guarda los valores del item.
        Almacena los valores anteriores a la modificacion.
        Incrementa la version de los valores.
        
        """
        #Hace backcup de los valores actuales que estan con uso actual =true del item
        item_part = get_object_or_404(Item, pk=int(self.kwargs.get('iditem',None))) 
        valores_item_part = ValoresItemView.qs_valores_actuales(item_part.pk)

        #puede que sea la version inicial de los valores del item
        if not valores_item_part[0].version == 0:
            #Cada valor del item se establece con valor de usoactual false
            #porque esta sera la version anterior
            for valor in valores_item_part:
                valor.pk = None # se fuerza a guardar un nuevo registro
                valor.usoactual = False
                valor.save()
                
        #recibe los parametros por post
        formset = self.ValoresFormSet(request.POST)
        
        if formset.is_valid():
            formset.save()
            #aun no sabemos como modificar instancias de un formset
            valores_item_part = ValoresItemView.qs_valores_actuales(item_part.pk)
            for valor in valores_item_part:
                valor.set_inc_version()
                valor.save()
            #actualiza la version del item
            item_part.version = valores_item_part[0].version 
            item_part.save()

        else:
            return render(request, TEMPL_FORMASIG, {'formset': formset, \
                        'action': reverse('valores_asignar',\
                        kwargs={'iditem':kwargs['iditem']}),\
                        'nodefault':'__panel.html'  })
 
        return redirect(get_url_edicion_actual(request,1))


class ValoresItemView(ListView):
    model = ItemAtributosValores
    template_name = 'desarrollo/lista_valores.html'
    
    def get_queryset(self):
        object_list = self.qs_valores_actuales(self.kwargs['iditem'])
        return object_list
     
    @classmethod
    def qs_valores_actuales(self, iditem):
        return ItemAtributosValores.objects.filter(Q(usoactual=True) & Q(iditem_id=iditem)) 


class ListaVersionesValor(ListView):
    """
    
    Lista las versiones de un item.
    
    """
    template_name = 'desarrollo/lista_versionesitem.html'
    model = ItemAtributosValores
    
    def get_queryset(self):
        object_list = ItemAtributosValores.objects.filter(iditem_id=self.kwargs['iditem'])
        return object_list

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['iditem'] = self.kwargs['iditem']
        return context



class RevertirValoreItem(View):
    """
    
    Vista que permite establecer una version anterior del item como actual.
    
    """
    template_name = 'desarrollo/form_confirm_revertir.html'
    
    def get(self,request,iditem, version):
        contex = {'iditem': iditem, 'version': version}
        return render(request, self.template_name, contex)
    
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        iditem = self.kwargs['iditem']
        version =self.kwargs['version']
        item = get_object_or_404(Item, pk=iditem)
        
        #Version anterior de los valores 
        # a los cuales tenemos que establecer usoactual falso
        vers_ant_valores = ItemAtributosValores.objects.filter(\
                                    Q(usoactual=True) & Q(iditem=item))
        for valitem in vers_ant_valores:
            valitem.usoactual = False
            valitem.save()
        
        num_vers = vers_ant_valores[0].version + 1  
        #nueva version nueva actual
        vers_actual = ItemAtributosValores.objects.filter(\
                                    Q(version=version) & Q(iditem=item))
        for valnuevo in vers_actual:
            valnuevo.pk = None
            valnuevo.usoactual = True
            #establece el numerode la nueva version
            valnuevo.version = num_vers
            valnuevo.save()
            
        item.version = num_vers
        item.save()
        messages.info(request, 'Operacion revertir realizada exitosamente sobre los valores')
        return redirect(reverse('valores_versiones',kwargs={'iditem': iditem}))
