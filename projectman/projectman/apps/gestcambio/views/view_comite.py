from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView  

from ..models import ComiteProyecto
from ..forms import ComiteProyectoForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from projectman.apps.admin.models import Proyecto
from django.contrib import messages 

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
    ocurrio_error = False
    
    def get_initial(self):
        self.proyecto_ob = get_object_or_404(Proyecto, pk=self.kwargs['idproyecto'])
        return { 'proyecto': self.proyecto_ob } # es como hacer #form.idfase=fase
    
    def get_success_url(self):
        return reverse('comite_listar', kwargs={'idproyecto':self.kwargs['idproyecto'] })
    
    def form_valid(self, form):
        #verifica que solo exista un solo registro del par (usuario, proyecto)
        miembro = ComiteProyecto.objects.filter(proyecto=form.instance.proyecto, \
                                                usuario =form.instance.usuario)
        if miembro.count()>0 :
            messages.error(self.request, 'ya existe este miembro para este proyecto')
            self.ocurrio_error = True
            return self.form_invalid(form)
        
        return CreateView.form_valid(self, form)
    

    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs) 
        context['action']= reverse('comite_crear',kwargs={'idproyecto':self.kwargs['idproyecto'] })
        if self.ocurrio_error:
            context['nodefault'] = '__panel.html'
        return context  


class ListarComiteProyectoView(ListView):
    """
    
    Lista los miembros del comite del proyecto
    
    """
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
    

class EliminarMiembroView(DeleteView):
    """
    
    Solicita confirmacion para eliminar un miembro del comite
    
    """
    model = ComiteProyecto
    template_name = 'form_confirm_delete.html'
    
    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('comite_eliminar', kwargs={'pk':self.kwargs['pk']})
        return context

