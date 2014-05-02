from django.forms import ModelForm

from django.forms import Select
from django.forms import HiddenInput
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms import PasswordInput
from models  import Proyecto
from models import Fase
from models import RolProyecto
from models import RolFases

class ProyectoIniciarForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['fechainicio', 'estado']
        #widgets = {"estado": HiddenInput()}
        
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
        
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name','is_active' ]
        widgets = {'password':PasswordInput()}
        
        labels = {
            'username': 'Usuario',
            'password ':'Contrasenha',
            'email' : 'Email',
            'first_name' : 'Nombre' ,
            'last_name' : 'Apellido' ,
            'is_active' : 'Activo'
        }
        help_texts = {
            'username': '',
            'password ':'',
            'email' : '',
            'first_name' : '' ,
            'last_name' : '' ,
            'is_active' : ''
        }


class PermisosRolesForm(ModelForm):
    class Meta:
        model = Group
        fields =['permissions']


class UsuarioRolForm(ModelForm):
    class Meta:
        model = User
        fields =['groups']
        labels = {
                  'groups':'Roles'
                  }
        help_texts = {
                      'groups':''
                    }



class ConsultaUsuarioForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions','is_staff','groups']
        
        labels = {
            'username' :'Usuario',
            'last_login':'Ultimo acceso',
            'is_superuser':'Super usuario',
            'first_name':'Nombres' , 
            'last_name':'Apellidos', 
            'email': 'Email', 
            'is_active':'Activo',
            'date_joined': 'Fecha alta'
            
        }
        help_texts = {
             'username' :'',
            'last_login':'',
            'is_superuser':'',
            'first_name':'' , 
            'first_name':'', 
            'email': '', 
            'is_active':'',
            'date_joined': ''
        }


class RolProyectoForm(ModelForm):
    class Meta:
        model = RolProyecto
        fields = ['rol','usuario','proyecto' ]
        labels = {'rol': 'Rol',
                  'usuario':'usuario',
                  'proyecto': 'Proyecto'
                  }


class RolFaseForm(ModelForm):
    """
    
    Formulario para la asignacion de fases a permisos por proyectos y usuarios.

    """
    class Meta:
        model = RolFases
        fields = ['fase', 'rolproyecto']
        widgets ={'rolproyecto':HiddenInput()}
