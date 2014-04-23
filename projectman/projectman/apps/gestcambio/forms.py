
from django.forms import HiddenInput
from django.forms import IntegerField
 
from django.forms import ModelForm 

from models import ComiteProyecto 


class ComiteProyectoForm(ModelForm):
    """ 
    
    Formulario de Carga y edicion de tipos de item 
    
    """
    fields = ['descripcion', 'proyecto']
    
    class Meta:
        model = ComiteProyecto

