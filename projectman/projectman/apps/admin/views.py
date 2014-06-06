# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login ,logout
#Models del modulo de autenticacion de django
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
# Views de tipo clase de django
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import  reverse
from django.db.models import Q

from datetime import date

#Modelos y formularios propios de la aplicacion
from models import Proyecto
from models import Fase 
from models import RolProyecto
from models import RolFases
from ..desarrollo.models  import Item 
from forms import ProyectoForm
from forms import FaseForm
from forms import UsuarioRolForm
from forms import ConsultaUsuarioForm
from forms import UserForm
from forms import RolProyectoForm 
from forms import RolFaseForm
from forms import ProyectoIniciarForm
from projectman.apps.desarrollo.views.view_oth import redirige_edicion_actual, get_url_edicion_actual



# Create your views here.

TEMPL_LOGINFORM = 'admin/form_login.html'
TEMPL_PROYECTOFORM = 'admin/form_proyecto.html'
TEMPL_PROYECTOLISTA = 'admin/lista_proyectos.html'
TEMPL_FASEFORM ='admin/form_fase.html'
TEMP_PERM_LIST ='admin/lista_permisos.html'
TEMPL_USERFORM = 'admin/form_user.html'
TEMPL_LIST_USER = 'admin/lista_usuarios.html'
TEMPL_ROLPERMS_FORM = "admin/form_rolespermisos.html" 
TEMPL_ROLES_LIST = "admin/lista_roles.html"
TEMPL_ASIG_ROL_USER = 'admin/form_asignarol.html'
TEMPL_DELCONFIRM = 'form_confirm_delete.html'
ABM_ACCIONES = ('editar', 'eliminar', 'crear')
#nombre de la variable de sesion que almacena los permisos
SESS_PERMS = 'permisos'

class IniciarProyecto(UpdateView):
    model = Proyecto
    form_class = ProyectoIniciarForm
    template_name = 'admin/form_confirm_iniciar.html'
    templ_base_error = None
    
    def post(self, request, *args, **kwargs):
        proy_iniciar = get_object_or_404(Proyecto, idproyecto=self.kwargs['pk'])
        proy_iniciar.estado = Proyecto.E_INICIADO
        proy_iniciar.fechainicio = date.today()
        proy_iniciar.save()
        return redirect (reverse('proyectos_asignados'))
         
         
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('iniciar_proyecto' , kwargs={'pk':self.kwargs['pk']} )
        return context
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return IniciarProyecto.form_invalid(self, form)

    #def form_valid(self, form):
        #form.instance.fechainicio = self.request.POST.get('fechainicio')
        #form.instance.estado = 'INI'
        #return IniciarProyecto.form_valid(self, form)
    
class CreaUsuarioView(CreateView):
    """
    Despliega el formulario para la carga de usuarios y 
    persiste un nuevo usuario.
    
    """
    model= User
    template_name = TEMPL_USERFORM
    form_class = UserForm
    templ_base_error = None
    
    def get_success_url(self):
        return reverse('usuario_listar')
    
    def get_context_data(self, **kwargs):
        context = super(CreaUsuarioView, self).get_context_data(**kwargs)
        context['action'] = reverse('usuario_crear')
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)
        
    def form_valid(self, form):
        #user = User.objects.create_user('x', 'x.com', self.request.POST.get('password'))
        form.instance.set_password(self.request.POST.get('password'))
        return CreateView.form_valid(self, form)
    
class ListarUsuarioView(ListView):
    """
    Despliega una lista de usuarios cargados en el sistema.
     
    Puede emitir una lista completa o bien una lista acotada por la busqueda 
    de usuarios por nombre y apellido.
    
    """
    model= User
    template_name = TEMPL_LIST_USER

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            
            object_list = self.model.objects.filter(Q(first_name__icontains=busqueda) | 
                                              Q(last_name__icontains=busqueda))
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list


class EliminarUsuarioView(DeleteView):
    """
    
    Solicita confirmacion para eliminar y elimina el usuario
    
    """
    model = User
    template_name = TEMPL_DELCONFIRM
    
    def get_success_url(self):
        return reverse('usuario_listar')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('usuario_elimina',kwargs={'pk':self.kwargs['pk']})
        return context


class EditaUsuarioView(UpdateView):
    """
    
    Permite modificar los atributos del usuario.
    
    """
    model = User
    form_class = UserForm
    template_name = TEMPL_USERFORM
    templ_base_error = None

    def get_success_url(self):
        return reverse('usuario_listar')
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('usuario_edita',kwargs={'pk':self.kwargs['pk']})
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

class ConsultaUsuarioView(UpdateView):
    """
    
    Consulta los datos de un usuario.
    Que Roles posee , y que permisos tiene asignados por medio de esos roles. 
    
    """
    model = User
    template_name = 'admin/detalle_usuario.html'
    form_class= ConsultaUsuarioForm


class EditaUsuarioRoles(UpdateView):
    """
    
    Permite asignar o desasignar roles a un usuario.
    
    """
    model = User
    form_class = UsuarioRolForm
    template_name = TEMPL_ASIG_ROL_USER

    def get_success_url(self):
        return reverse('usuario_listar')
    
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['idgrupo'] = self.kwargs['pk']
        return context


@require_POST
def autenticar(request):
    """
    
    Autentica a un usuario con el par (username, password).
    
    """
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
    """
    
    Cierra la sesion del usuario.
    
    """
    logout(request)
    return redirect('/admin/login/')


@login_required
def proyectos_abm(request, accion=None,idproyecto=None ):
    """
    
    Punto de entrada para crear , modificar o borrar proyectos. 
    
    """
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
    #return render(request,TEMPL_PROYECTOLISTA, { 'lista_proyectos' : lista_proyectos })
    
    messages.info(request,'Debe asignar un rol al proyecto recien creado'  )
    return redirect(reverse('proyectos_asignados'))


@login_required
def fases_abm(request,accion=None, idelemento=None):
    """
    
    Acepta peticiones de Agregar , modificar y eliminar una fase, 
    y mostrar el template con el formulario para el efecto 
    
    """

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
    """
    
    Lista los permisos que corresponden a una rol en particular
    
    """
    model= Permission 
    template_name= TEMP_PERM_LIST

    def get_queryset(self):
        grupo = Group.objects.filter(pk=self.kwargs['pk'])
        permisos = Permission.objects.filter(group__in=grupo)
        return permisos


class CreaRolPermisosView(CreateView):
    """
    
    Crea un Rol nuevo permitiendo asignar los permisos a este nuevo rol.
    
    """
    model = Group
    template_name = TEMPL_ROLPERMS_FORM
    templ_base_error = None
    mensaje = "El formulario tiene datos incorrectos o incompletos!"
    
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
            context['errormensaje'] = self.mensaje
        return context


class EditaRolPermisosView(UpdateView):
    """
    
    Permite editar un Rol en particular.
    Permite asignar y desasignar permisos 
        
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
    """
    
    Lista todos los roles o el resultado de una busqueda. 
    La busqueda se realiza por el nombre del rol 
    
    """
    model = Group
    template_name = TEMPL_ROLES_LIST

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(name__icontains=busqueda)
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context


class EliminaRolPermisosView(DeleteView):
    """
    
    Permite eliminar un rol , previa solicitud de confirmacion.
    
    """
    model = Group
    template_name = TEMPL_DELCONFIRM

    def get_success_url(self):
        return reverse('rol_permisos_lista')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_permisos_elimina',kwargs={'pk':self.kwargs['pk']})
        return context


class AsignaRolProyectoView(CreateView):
    """
    
    Permite asignar un rol a un proyecto y a un usuario.
    
    """
    model = RolProyecto
    form_class = RolProyectoForm
    template_name = 'admin/form_rolproyecto.html'
    templ_base_error = None
    
    def get_success_url(self):
        return reverse('rol_proyecto_listar')
    
    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_proyecto_crear')
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context
    
    def form_valid(self, form):
        #verificamos que aun no este asignado:
        #el usuario  a un  proyecto con algun rol
        qs = RolProyecto.objects.filter(usuario=form.instance.usuario
                                   ).filter(proyecto=form.instance.proyecto)
        #si ya esta asignado enviamos un mensaje de error
        if (qs.count() > 0):
            messages.error(self.request, 'Esta asignacion ya existe, solo puede asignar \
            un rol a un usuario para un proyecto.')
            self.templ_base_error = "__panel.html"
            return self.form_invalid(form)
        return CreateView.form_valid(self, form)
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)


class ListaRolProyectoView(ListView):

    model = RolProyecto
    template_name = 'admin/lista_rolesproyectos.html'
    lista_fases = None
     
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['lista_fases'] = self.lista_fases
        if self.kwargs.get('idrolproyecto'):
            context['idrolproyecto'] = int(self.kwargs.get('idrolproyecto'))
        return context
    
    def get_queryset(self):
        #obtiene las relaciones con el modelo rolproyecto
        if self.kwargs.get('idrolproyecto'):
            relacion_proy = get_object_or_404(RolProyecto,\
                                              pk=self.kwargs.get('idrolproyecto'))
            relacion_fase = RolFases.objects.filter(rolproyecto=relacion_proy)
            #self.lista_fases = Fase.objects.filter(rolfases__in=relacion_fase)
            self.lista_fases = relacion_fase
            
        return ListView.get_queryset(self)



class EliminaRolProyectoView(DeleteView):
    """
    
    Permite borrar una asignacion de : un rol a un proyecto y a un usuario.
    Recibe como parametro el identificador de la asignacion
    
    """
    model = RolProyecto
    template_name = TEMPL_DELCONFIRM

    def get_success_url(self):
        return reverse('rol_proyecto_listar')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_proyecto_eliminar',
                                    kwargs={'pk':self.kwargs['pk']})
        return context


class ListaProyectosUsuario(ListView):
    """ 
    
    Lista solo los proyectos permitidos para el usuario 
    
    """
    model = RolProyecto
    template_name = 'admin/lista_proyectos.html'
    sess_perms = SESS_PERMS
    

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context

    def get_queryset(self):
        #obtiene todos los proyectos asignados al usuario
        proyectos = Proyecto.objects.filter(rolproyecto__usuario=self.request.user)
        busqueda = self.request.GET.get('busqueda','')
        if busqueda:
            proyectos = proyectos.filter(nombre__icontains=busqueda)
            messages.info(self.request, 'Resultados..nombres con : ' + busqueda)
        if proyectos.count() < 1 :
            messages.info(self.request,'No tiene asignado proyecto alguno,\
                contacte con el administrador')
        object_list = proyectos
        return object_list


class AsignaFaseRolView(CreateView):
    """
    
    Asigna un (rol , usuario , proyecto) a una fase del proyecto.
    
    """
    model = RolFases
    form_class = RolFaseForm
    templ_base_error = None
    rolproyecto = None 
    template_name = 'admin/form_rolfase.html'
    
    def get_initial(self):
        #consulta la relacion rolproyecto por medio de su id
        self.rolproyecto = get_object_or_404(RolProyecto,pk=self.kwargs['idrolproyecto']) 
        return { 'rolproyecto': self.rolproyecto }

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)
    

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_fase_crear',\
                                kwargs={'idrolproyecto':self.kwargs['idrolproyecto'] })
        if self.templ_base_error:
            context['nodefault']= self.templ_base_error
        return context
    
    def get_form(self, form_class):
        form = CreateView.get_form(self, form_class)
        #obtiene el proyecto
        self.rolproyecto = get_object_or_404(RolProyecto, pk=self.kwargs['idrolproyecto'])
        #obtiene solo las fases que tiene el proyecto. en lugar de todas las fases.
        proyecto = get_object_or_404(Proyecto,pk=self.rolproyecto.proyecto_id )
        form.fields['fase'].queryset = Fase.objects.filter(idproyecto=proyecto)
        return form
    
    def get_success_url(self):
        return reverse('rol_proyecto_fase',kwargs={'idrolproyecto':self.kwargs['idrolproyecto']})

    def form_valid(self, form):
        #verificamos que aun no este asignado:
        #el usuario  a un  proyecto con algun rol
        
        qs = RolFases.objects.filter(rolproyecto_id=self.kwargs['idrolproyecto']).\
            filter(fase=form.instance.fase)
            
        #si ya esta asignado enviamos un mensaje de error
        if (qs.count() != 0):
            messages.error(self.request, 'Este permiso para la fase ya existe, para este usuario')
            self.templ_base_error = "__panel.html"
            return self.form_invalid(form)
        return CreateView.form_valid(self, form)


class EliminaRolFaseView(DeleteView):
    """
    
    Recibe como parametro el identificador de la asignacion de asignacion a nivel de fase.
    
    """
    model = RolFases
    template_name = TEMPL_DELCONFIRM

    def get_success_url(self):
        return reverse('rol_proyecto_listar')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('rol_fase_eliminar',
                                    kwargs={'pk':self.kwargs['pk']})
        return context


class ListaRolFasesView(ListView):
    """ 
    
     
    
    """
    model = RolFases
    template_name = 'admin/lista_rolesfases.html'

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context

    def get_queryset(self):
        #obtiene primero la relacion entre el proyecto el usuario y el rol
        rolproyp = get_object_or_404(RolProyecto, pk=self.kwargs['idrolproyecto'])
        #consulta las fases que pertenecen a la relacion 
        fases = Fase.objects.filter(rolfases__rolproyecto=rolproyp)
        object_list = fases
        return object_list


class FinalizaFase(View):
    template_name ='form_confirm_accion.html'

    def post(self, request, *args, **kwargs):
        """

        Establece el estado de la fase a finalizada

        """
        #establece el estado de la solicitud a enviada
        fase_fin = get_object_or_404(Fase, pk=self.kwargs['pk'])
        #serie de validaciones 
        (validez, mensaje ) = self.valid_finalizar_fase(self.kwargs['pk'])
        
        if not validez:
            messages.error(request,mensaje )
            return redirect(get_url_edicion_actual(request, 1))
        
        fase_fin.estado = Fase.E_FINALIZADO
        fase_fin.save()
        messages.info(request, mensaje )
        return redirect(get_url_edicion_actual(request, 1))

    def get(self,request, pk ):
        """

        Despliega el formulario de confirmacion generico.
        Con valores particulares para finalizar la fase.

        """
        return render(request, self.template_name, {'action':reverse('finalizar_fase',\
                                                              kwargs={'pk':pk } ),\
                                             'titulo': 'Finalización de fase',\
                                             'texto': '¿Está seguro que desea finalizar la fase?',\
                                             'value': 'Aceptar' })
    
    def valid_finalizar_fase(self, idfase):
        """
        
        Valida los elementos internos de la fase antes de finalizar
        
        """
        items_fase =Item.objects.filter(idfase_id=idfase).exclude(estado=Item.E_ELIMINADO)
        
        #verifica que exista al menos un item  en la fase 
        if items_fase.count() < 1:
            return (False, 'ERROR : Verifique que la fase posea al menos un ítem y este en una línea base' )
        #verifica que todos los items esten en alguna linea base 
        if  items_fase.exclude(estado=Item.E_BLOQUEADO).count() > 0 :
            return (False, 'ERROR : Verifique que todos los items esten en línea base' )
        
        return (True , 'EXITO : Fase finalizada correctamente ')


class FinalizaProyecto(View):
    """
    
    Vista que permite Finalizar el proyecto.
    Valida que las fases esten finalizadas.
    
    """
    template_name ='form_confirm_accion.html'

    def post(self, request, *args, **kwargs):
        """

        Establece el estado del proyecto a finalizado

        """
        #establece el estado de la solicitud a enviada
        proyecto_fin = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        #serie de validaciones 
        (validez, mensaje ) = self.valid_finalizar_proyecto(self.kwargs['pk'])
        
        if not validez:
            messages.error(request,mensaje )
            return redirect(get_url_edicion_actual(request, 0))
        
        #valida el estado del proyecto 
        if proyecto_fin.estado != Proyecto.E_INICIADO:
            messages.error(request, 'ERROR : El proyecto no fue iniciado o ya fue finalizado' )
            return redirect(get_url_edicion_actual(request, 0))
        
        proyecto_fin.estado = Proyecto.E_FINALIZADO
        proyecto_fin.fechafin = date.today()
        proyecto_fin.save()
        messages.info(request, mensaje )
        return redirect(get_url_edicion_actual(request, 0))

    def get(self,request, pk ):
        """

        Despliega el formulario de confirmacion generico.
        Con valores particulares para finalizar el proyecto.

        """
        return render(request, self.template_name, {'action':reverse('finalizar_proyecto',\
                                                              kwargs={'pk':pk } ),\
                                             'titulo': 'Finalización del proyecto',\
                                             'texto': '¿Está seguro que desea finalizar el proyecto?',\
                                             'value': 'Aceptar' })
    @classmethod
    def valid_finalizar_proyecto(self, idproyecto):
        """
        
        Valida la Finalizacion el proyecto.
        Retorna verdadero si es posible finalizar el proyecto.
        
        """
        lista_fases = Fase.objects.filter(idproyecto_id=idproyecto)
        for fase_i in lista_fases:
            if fase_i.estado != Fase.E_FINALIZADO:
                return (False, 'ERROR : Debe finalizar todas las fases antes de finalizar el proyecto')
        
        return (True, 'Proyecto Finalizado correctamente')
    
