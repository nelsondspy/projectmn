# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST 
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout 
from django.contrib import messages 
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.models import Permission
from django.views.generic import ListView 
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView #importar la clase de la que hereda
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.contrib.auth.models import User
from django.core.urlresolvers import  reverse



from models import Proyecto
from models import Fase 
from forms import ProyectoForm
from forms import FaseForm
from projectman.apps.desarrollo.views import redirige_edicion_actual 

from django.contrib.auth.decorators import login_required
from forms import UserForm
# Create your views here.

TEMPL_LOGINFORM = 'admin/form_login.html'
TEMPL_PROYECTOFORM = 'admin/form_proyecto.html'
TEMPL_PROYECTOLISTA = 'admin/form_proyectoedit.html'
TEMPL_FASEFORM ='admin/form_fase.html'
TEMP_PERM_LIST ='admin/lista_permisos.html'
TEMPL_USERFORM = 'admin/form_user.html'
TEMPL_LIST_USER = 'admin/lista_usuarios.html'
TEMPL_ROLPERMS_FORM = "admin/form_rolespermisos.html" 
TEMPL_ROLES_LIST = "admin/lista_roles.html"
TEMPL_DELCONFIRM = 'form_confirm_delete.html'
ABM_ACCIONES = ('editar', 'eliminar', 'crear')

class CreaUsuarioView(CreateView):
    model= User
    template_name = TEMPL_USERFORM
    form_class = UserForm
    templ_base_error = None
    
    def get_success_url(self):
        return reverse('usuario_listar')
    
    def get_context_data(self, **kwargs):
        context = super(CreaUsuarioView, self).get_context_data(**kwargs)
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)
    
    
class ListarUsuarioView(ListView):
    model= User
    template_name = TEMPL_LIST_USER
        

    
@require_POST
def autenticar(request):
    usuario = request.POST['username']
    contrasenha = request.POST['password']
    usuario = authenticate(username=usuario, password = contrasenha)
    if usuario is not None :
        if usuario.is_active:
            login(request, usuario)
            return render(request,'__panel.html')
        else:
            messages.error(request, 'Usuario inactivo')
            return render(request , TEMPL_LOGINFORM )
    else:
        messages.error(request, 'Contreña o usuario , incorrecto')
        return render(request,TEMPL_LOGINFORM)

@require_GET
def login_form(request):
    return render(request,TEMPL_LOGINFORM, {'mensaje_error':''})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('/admin/login/')
        


"""Punto de entrada para crear , modificar o borrar proyectos """
@login_required
def proyectos_abm(request, accion=None,idproyecto=None ):
    form = ProyectoForm()
    if accion in ABM_ACCIONES :
        if accion == 'crear':
            form = ProyectoForm()
            return render(request, TEMPL_PROYECTOFORM, {'form': form,'accion':accion}, 
                          context_instance=RequestContext(request))
            
        if not idproyecto is None:
            proyecto = Proyecto.objects.get(pk=idproyecto)
        if accion == 'eliminar':
            proyecto.delete()
        if accion =='editar':
            form = ProyectoForm(instance=proyecto)
            return render(request, TEMPL_PROYECTOFORM, {'form': form,'accion':accion}, 
                          context_instance=RequestContext(request))
    lista_proyectos = Proyecto.objects.all()
    #Crea o modifica un proyecto existente 
    if request.method == 'POST':
        instancia = None
        idpro = request.POST.get('idproyecto',None)
        if not idpro is None : 
            try :
                instancia = Proyecto.objects.get(pk=idpro)
            except instancia.DoesNotExist:
                instancia = None
        form = ProyectoForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
        else:
            return render(request,TEMPL_PROYECTOFORM, {'nodefault':'__panel.html','form':form})
    return render(request,TEMPL_PROYECTOLISTA, { 'lista_proyectos' : lista_proyectos })
    
    
"""Acepta peticiones de Agregar , modificar y eliminar una fase, 
   y mostrar el template con el formulario para el efecto """
@login_required
def fases_abm(request,accion=None, idelemento=None):
    if accion in ABM_ACCIONES:
        if accion == 'eliminar':
            fase = Fase.objects.get(pk=idelemento) 
            fase.delete()
            return redirige_edicion_actual(request)
             
        if accion =='editar' :
            fase = Fase.objects.get(pk=idelemento) 
            faseform = FaseForm(instance=fase)
            return render_to_response(TEMPL_FASEFORM, {'faseform': faseform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
        if accion == 'crear':
            proyecto = Proyecto.objects.get(pk=idelemento) 
            fase = Fase(idproyecto=proyecto)  
            faseform = FaseForm(instance=fase)
            return render_to_response(TEMPL_FASEFORM, {'faseform': faseform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
    if request.method == 'POST':
        #Edita una fase existente, o crear unan nueva
        idproyecto_post = request.POST.get('idproyecto',None)
        idfasepost = request.POST.get('idfase',None)
        if idfasepost:
            instancia_fase = Fase.objects.get(pk=idfasepost)
        else: 
            proyecto = Proyecto.objects.get(pk=idproyecto_post)
            instancia_fase = Fase(idproyecto=proyecto)
        faseform = FaseForm(request.POST, instance=instancia_fase)
        if faseform.is_valid():
            faseform.save()     
            return redirige_edicion_actual(request)
        else:
            return render(request ,TEMPL_FASEFORM,{'nodefault':'__panel.html', 'faseform': faseform})

class ListaPermisosView(ListView):
    """Lista de permisos  """
    model= Permission 
    template_name= TEMP_PERM_LIST


class CreaRolPermisosView(CreateView):
    model = Group
    template_name = TEMPL_ROLPERMS_FORM
    templ_base_error = None
    
    def get_success_url(self):
        return reverse('rol_permisos_lista')
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)
     
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_permisos')
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context


class EditaRolPermisosView(UpdateView):
    """Vista que permite editar un permiso.
    
    
    """
    model = Group
    template_name = TEMPL_ROLPERMS_FORM
    templ_base_error = None
    def get_success_url(self):
        return reverse('rol_permisos_lista')
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_permisos_edita',kwargs={'pk':self.kwargs['pk']})
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

class ListaRolPermisosView(ListView):
    model = Group
    template_name = TEMPL_ROLES_LIST
 
    def get_queryset(self):
        """Lista todos los roles o el resultado de la busqueda 
        de un rol por su nombre""" 
        try:
            name = self.kwargs['busqueda']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(name__icontains = name)
            if object_list.count() < 1:
                object_list = self.model.objects.all()
                messages.info(self.request, "No se han encontrado coindicencias: " + name)
            else:
                messages.info(self.request, "resultados de la busqueda: " + name)
        else:
            object_list = self.model.objects.all()
        return object_list


class EliminaRolPermisosView(DeleteView):
    model = Group
    template_name = TEMPL_DELCONFIRM
    def get_success_url(self):
        return reverse('rol_permisos_lista')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_permisos_elimina',kwargs={'pk':self.kwargs['pk']})
        return context

