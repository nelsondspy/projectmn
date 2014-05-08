
from django.forms import HiddenInput
from django.forms import IntegerField
from django.forms import CheckboxSelectMultiple 

from django.forms import ModelForm 

from models import ComiteProyecto 

from models import LineaBase
from models import SolicitudCambio


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
        


class SolicitudCambioForm(ModelForm):
        class Meta:
            model = SolicitudCambio 
            fields = ['comentarios', 'solicitante', 'items', 'estado','fecha_aprobacion' ]
            widgets= {'items':CheckboxSelectMultiple() }
            

