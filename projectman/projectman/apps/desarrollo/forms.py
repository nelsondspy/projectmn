

from django.forms import HiddenInput
from django.forms import IntegerField
    
 
from django.forms import ModelForm 
from models import ItemTipos
from models import ItemAtributos
from models import Item
from models import ItemAtributosValores
 


class ItemTiposForm(ModelForm):
    """ Formulario de Carga y edicion de tipos de item """
    #idfase = IntegerField(widget=HiddenInput)
    
    class Meta:
        model = ItemTipos
        fields = ['idfase', 'nombre', 'descripcion']
        widgets = {"idfase": HiddenInput()}


class AtributosTiposForm(ModelForm):
    """Formulario de carga y edicion de """
    
    class Meta:
        model = ItemAtributos
        fields =['nombre','descripcion', 'tipodato', 'idtipoitem' ]
        widgets ={'idtipoitem':HiddenInput()}


class ItemForm(ModelForm):
    """
    Formulario del modelo Item 
    preve la creacion condicional de controles para crear nuevos items en una fase
    o bien editar existentes  

    """
    
    class Meta:
        model = Item
        fields=['nombre']

   
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance and instance.iditem:
            self.fields['iditem']=IntegerField(widget=HiddenInput)
            self.fields['iditem'].initial=instance.iditem
        if instance and instance.idfase:
            self.fields['idfase']=IntegerField(widget=HiddenInput)
            self.fields['idfase'].initial=(instance.idfase).idfase
             


class ItemFormN(ModelForm):
    class Meta:
        model = Item
        fields=['nombre', 'idfase','version','idtipoitem']
        widgets ={'idfase':HiddenInput()}


class ItemValoresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemValoresForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance :
            self.fields['idatributo'].label=instance.idatributo.__str__()
            
        
    class Meta:
        model = ItemAtributosValores
        fields = ['iditem','idatributo', 'valor']
        widgets ={'iditem':HiddenInput(), 'idatributo':HiddenInput()}
