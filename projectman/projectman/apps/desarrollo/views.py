from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.views.generic import View
from django.contrib.auth.decorators import login_required
 
from models import Fase , Item  
from projectman.apps.admin.models import  Proyecto
from forms import ItemForm
from models import ItemTipos
from forms import ItemTiposForm 
from django.template import RequestContext

SESS_IDPROYECTO = 'idproyecto'
SESS_IDFASE = 'idfase'
TEMPL_PANEL = '__panel.html'
TEMPL_EXPLORADOR = 'explorador_comp.html'

@login_required
def mostrar_panel(request):
    return render(request, TEMPL_PANEL)



"""Redirige a la vista que muestra el proyecto/fase/item que se esta editando
actualmente, segun las variables de sesion, por niveles de url 
"""
def redirige_edicion_actual(request, nivel=0):
    #por defecto el nivel 0 es el proyecto
    url_redirigir = '/desarrollo/componentes/'+ request.session[SESS_IDPROYECTO]
    #el nivel 1 es la fase
    if nivel == 1: 
        url_redirigir  += '/'+request.session[SESS_IDFASE]
    #el nivel 2 es el item 
    return redirect(url_redirigir)


""""Explorador de componentes de forma jerarquica permitira listar fases, los items de una fase
los astributos de una fase """
@login_required
def editor_componentes(request, idproyecto=None, idfase=None):
    proyecto = Proyecto.objects.get(pk=idproyecto)
    request.session[SESS_IDPROYECTO] = idproyecto
    request.session[SESS_IDFASE] = None
    #lista las fases del proyecto  
    lista_fases = Fase.objects.filter(idproyecto=idproyecto)
    #lista de items de una fase seleccionada ( recibida como parametro) 
    lista_items = None
    if idfase:
        request.session[SESS_IDFASE] = idfase
        lista_items = Item.objects.filter(idfase=idfase)
        idfase = int(idfase) # en la plantilla se requier el valor entero no el unicode
        
    return render(request , TEMPL_EXPLORADOR , {'proyecto': proyecto , 'idfase':idfase,
                    'lista_fases':lista_fases , 'lista_items':lista_items})


@login_required
def procesa_item(request, accion=None,idelemento=None):
    if accion in ('editar', 'eliminar', 'crear'):
        if accion == 'eliminar':
            item = Item.objects.get(pk=idelemento) 
            item.delete()
            return redirige_edicion_actual(request, nivel=1)
        if accion =='editar' :
            item  = Item.objects.get(pk=idelemento) 
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
        if accion == 'crear':
            fase = Fase.objects.get(pk=idelemento) 
            item = Item(idfase=fase)
            itemform = ItemForm(instance=item)
            return render_to_response('form_item.html', {'itemform': itemform , 'accion':accion} , 
                                      context_instance=RequestContext(request))
    if request.method == 'POST':
        #Edita una fase existente, o crear unan nueva
        idfasepost = request.POST.get('idfase',None)
        iditempost = request.POST.get('iditem',None)
        if iditempost:
            instancia_item = Item.objects.get(pk=iditempost)
        if idfasepost:
            fase = Fase.objects.get(pk=idfasepost)
            instancia_item = Item(idfase=fase)
            instancia_item.sigte_numero()
        itemform = ItemForm(request.POST, instance=instancia_item)
        if itemform.is_valid():
            itemform.save()     
            return redirige_edicion_actual(request, nivel=1)


class EditForm(View):
    template = ""
    formulario = None
    modelo = None
    claveform = ""
    modelo_foraneo = None
    atributo_foraneo = ''
    LSACCIONES = ('crear' , 'editar', 'eliminar')
    
    
    def get(self, request, accion=None, idelemento=None):
        if accion in self.LSACCIONES:
            #editar 
            if accion == self.LSACCIONES[1]:               
                elemento = self.modelo(pk=idelemento)
                form = self.formulario(elemento)

            #accion crear
            if accion == self.LSACCIONES[0]:
                objetoforaneo = self.modelo_foraneo.objects.get(pk=idelemento)
                elemento = self.modelo()
                setattr(elemento, self.atributo_foraneo , objetoforaneo )
                 
            return render(request, self.template, {self.claveform :form })
