from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import CharField
from django.forms import ValidationError
import re
from datetime import datetime 
from django.forms import ModelForm 
from models import ItemTipos
from models import ItemAtributos
from models import Item
from models import ItemAtributosValores
from models import ItemRelacion
from projectman.apps.admin.models import  Fase


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
    
    tipodato = CharField (widget=HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super(ItemValoresForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance :
            self.fields['idatributo'].label=instance.idatributo.__str__()
            self.fields['tipodato'].initial = instance.idatributo.tipodato

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        atributo = self.cleaned_data['idatributo']
        
        #valida el valor de tipo de dato numerico
        #soporta enteros y decimales con signo
        num_reg = re.compile('(\-|\+)?[0-9]+(\.[0-9])?$')
        if atributo.tipodato == ItemAtributos.T_NUM:
            if num_reg.match(valor) is None:
                raise ValidationError("Ingrese un numero ")

        #valida el valor de un tipo de dato fecha  
        if atributo.tipodato == ItemAtributos.T_DATE:
            try:
                datetime.strptime(valor, "%d/%m/%Y")
                return valor 
            except ValueError:
                raise ValidationError("Ingrese una fecha valida")
        return valor
        
    class Meta:
        model = ItemAtributosValores
        fields = ['iditem', 'idatributo', 'valor']
        widgets ={'iditem':HiddenInput(), 'idatributo':HiddenInput()}
        


class ItemRelacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemRelacionForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance :
            items = Item.objects.all()
            self.fields['origen'].choices = [(item.pk,'['+ item.idfase.__str__()+'] ' + item.nombre\
                                              ) for item in items]
    
    class Meta:
        model = ItemRelacion
        fields = ['tipo','origen','destino']
