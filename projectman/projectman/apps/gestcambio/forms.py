
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import CheckboxSelectMultiple 
from django.forms import ModelMultipleChoiceField
from django.forms import ModelForm 
from django.forms.models import inlineformset_factory 
from models import ComiteProyecto 

from models import LineaBase


class ComiteProyectoForm(ModelForm):
    """ 
    
    Formulario de Carga y edicion de tipos de item 
    
    """
    fields = ['descripcion', 'proyecto']
    
    class Meta:
        model = ComiteProyecto
        fields = ['proyecto', 'usuario']


class LineaBaseForm(ModelForm):
    """

    Formulario que permite cargar los datos del modelo LineaBase

    """
    
    class Meta:
        model = LineaBase
        fields = ['descripcion', 'fase', 'items']
        widgets= {'fase' : HiddenInput(), 'items':CheckboxSelectMultiple() }
        

