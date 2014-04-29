from django.views.generic.edit import CreateView
from django.views.generic import ListView  

from ..models import ComiteProyecto
from ..forms import ComiteProyectoForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from projectman.apps.admin.models import Proyecto

TEMPL_LISTACOMITE ='gestcambio/lista_comite.html'

class CrearComiteProyectoView(CreateView):
    """
    Permite la creacion de un comite para un proyecto.
    
    Valida que para un proyecto solo pueda crearse un comite.
    
    """
    models = ComiteProyecto
    form_class = ComiteProyectoForm
    template_name= 'gestcambio/form_comiteproyecto.html'
    proyecto_ob = None
    
    def get_initial(self):
        self.proyecto_ob = get_object_or_404(Proyecto, pk=self.kwargs['idproyecto'])
        return { 'proyecto': self.proyecto_ob } # es como hacer #form.idfase=fase
    
    def get_success_url(self):
        return reverse('comite_listar', kwargs={'idproyecto':self.kwargs['idproyecto'] })

    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs) 
        context['action']= reverse('comite_crear',kwargs={'idproyecto':self.kwargs['idproyecto'] })
        return context  
    
class ListarComiteProyectoView(ListView):
    models = ComiteProyecto
    template_name = TEMPL_LISTACOMITE
    
    def get_queryset(self):
        object_list = ComiteProyecto.objects.filter(proyecto_id=self.kwargs['idproyecto'])
        print "lista comite: "
        print (object_list)
        return object_list
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['idproyecto'] = self.kwargs['idproyecto']
        return context