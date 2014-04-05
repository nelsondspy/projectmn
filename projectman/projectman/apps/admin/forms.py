from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.forms import Select
from django.forms import HiddenInput
from django.forms import IntegerField
from models  import Proyecto
from models import Fase

class ProyectoForm(ModelForm):
    
    #si existe alguna instancia para el form , crea un InputField con el valor del id
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance and instance.idproyecto:
            self.fields['idproyecto'] = IntegerField(widget=HiddenInput)
            self.fields["idproyecto"].initial=instance.idproyecto
           
    class Meta:
        model = Proyecto
        fields = ['idproyecto','nombre', 'descripcion']
        widgets = {'idtipo': Select(attrs={'class': 'select'})  }

class FaseForm(ModelForm):
    # 
    def __init__(self, *args, **kwargs):
        super(FaseForm, self).__init__(*args, **kwargs)
        instance = getattr(self,'instance',None)
        if instance and instance.idfase:
            self.fields['idfase']=IntegerField(widget=HiddenInput)
            self.fields['idfase'].initial=instance.idfase
        if instance and instance.idproyecto:
            self.fields['idproyecto']=IntegerField(widget=HiddenInput)
            self.fields['idproyecto'].initial=(instance.idproyecto).idproyecto
    class Meta:
        model = Fase
        fields = ['nombre','descripcion']
        widgets     = {'idproyecto': Select(attrs={'class': 'input'})}


