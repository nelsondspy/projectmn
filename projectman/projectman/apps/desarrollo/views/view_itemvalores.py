from django.views.generic import View

from django.shortcuts import render_to_response, render
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.db.models import Q

from ..models import ItemAtributosValores
from ..models import ItemTipos
from ..models import ItemAtributos
from ..forms import ItemValoresForm
from ..models import Item

TEMPL_FORMASIG='desarrollo/form_itemvaloresatributos.html'

def asignar_valores(request,iditem):

    if request.method == "GET" : 
        item = get_object_or_404(Item, pk=iditem)
        #primero intancia valores de supertipos, los supertipos son 
        tipo_default = ItemTipos.objects.filter(es_supertipo=True)
        atributos = ItemAtributos.objects.filter(idtipoitem=tipo_default)
        for atrr in atributos:
            atributovalor = ItemAtributosValores()
            atributovalor.idatributo = atrr 
            atributovalor.iditem = item
            atributovalor.valor = '0'
            atributovalor.usoactual = True
            atributovalor.save()
        ValoresFormSet = modelformset_factory(model=ItemAtributosValores, form=ItemValoresForm)
        formset = ValoresFormSet(queryset=ItemAtributosValores.objects.filter(iditem=iditem))
        
        return render_to_response(TEMPL_FORMASIG,{'formset': formset})



class AsignaValoresItem(View):
    
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
                atributovalor.valor = '0'
                atributovalor.save()
        #pos insercion la lista de atributos con valores intanciados  del item
        lista_valores = ItemAtributosValores.objects.filter(iditem=item)
        formset = self.ValoresFormSet(queryset=lista_valores)
        #return render_to_response(TEMPL_FORMASIG,{'formset': formset})
        return render(request, TEMPL_FORMASIG, {'formset': formset })
    
    def post(self, request, *args, **kwargs):
        """
        
        Metodo que guarda los valores del item
        
        """
        formset = self.ValoresFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        return render(request, TEMPL_FORMASIG, {'formset': formset })

