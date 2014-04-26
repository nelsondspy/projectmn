
from django.forms import HiddenInput
from django.forms import IntegerField
 
from django.forms import ModelForm 

from models import ComiteProyecto 
from models import LineaBaseItem

class ComiteProyectoForm(ModelForm):
    """ 
    
    Formulario de Carga y edicion de tipos de item 
    
    """
    fields = ['descripcion', 'proyecto']
    
    class Meta:
        model = ComiteProyecto
        fields = ['proyecto', 'usuario']


class LineaBaseItemForm(ModelForm):
    class Meta:
        model = LineaBaseItem
