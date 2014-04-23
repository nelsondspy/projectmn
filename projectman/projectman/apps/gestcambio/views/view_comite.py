from django.views.generic.edit import CreateView
 

from ..models import ComiteProyecto
from ..forms import ComiteProyectoForm


class CrearComiteProyectoView(CreateView):
    """
    Permite la creacion de un comite para un proyecto.
    
    Valida que para un proyecto solo pueda crearse un comite.
    
    """
    models = ComiteProyecto
    form_class = ComiteProyectoForm
    template_name= 'gestcambio/form_comiteproyecto.html'
