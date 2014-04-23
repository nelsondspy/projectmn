

from django.forms import HiddenInput
from django.forms import IntegerField
 
from django.forms import ModelForm 
from models import ItemTipos
from models import ItemAtributos
from models import Item

 


class ItemTiposForm(ModelForm):
    """ Formulario de Carga y edicion de tipos de item """
    #idfase = IntegerField(widget=HiddenInput)
    fields = ['nombre', 'descripcion']
    
    class Meta:
        model = ItemTipos
        widgets = {"idfase": HiddenInput()}


class AtributosTiposForm(ModelForm):
    """Formulario de carga y edicion de """
    
    class Meta:
        model = ItemAtributos
        fields =['nombre','descripcion', 'tipodato', 'idtipoitem' ]
        widgets ={'idtipoitem':HiddenInput()}


"""Formulario del modelo Item 
preve la creacion condicional de controles para crear nuevos items en una fase
o bien editar existentes  
"""
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields=['descripcion','version', 'idtipoitem']
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance and instance.iditem:
            self.fields['iditem']=IntegerField(widget=HiddenInput)
            self.fields['iditem'].initial=instance.iditem
        if instance and instance.idfase:
            self.fields['idfase']=IntegerField(widget=HiddenInput)
            self.fields['idfase'].initial=(instance.idfase).idfase 

