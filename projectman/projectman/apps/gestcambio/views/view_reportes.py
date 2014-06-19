from easy_pdf.views import PDFTemplateView
from django.views.generic import View
from ..models import SolicitudCambio
from ..forms import ReporteSolicForm
from django.shortcuts import render

class ListaSolicitudesPDF(PDFTemplateView):
    """
    
    Vista que permite permite visualizar una lista de solicitudes en formado pdf.
    Admite las siguientes variantes:
    
    lista general de solicitudes
    lista de solicitudes por estado. 
    lista de solicitudes por solicitante
    
    """
    template_name = "gestcambio/rpt_lista_solicitudes.html"
    EST_SOLICITUD = {'E_APROBADO': SolicitudCambio.E_APROBADO, \
                         'E_RECHAZADO': SolicitudCambio.E_RECHAZADO,\
                         'E_ENVIADO': SolicitudCambio.E_ENVIADO, \
                         'E_TERMINADO': SolicitudCambio.E_TERMINADO,\
                         'E_BORRADOR': SolicitudCambio.E_BORRADOR }
    title= ''
    sub_titulo = ''
    lista_solicitudes = None

    def get_context_data(self, **kwargs):
        return super(ListaSolicitudesPDF, self).get_context_data(
            pagesize="A4",
            title=self.title,
            sub_titulo=self.sub_titulo,
            lista_solicitudes=self.lista_solicitudes,
            EST_SOLICITUD = self.EST_SOLICITUD
        )
    
    def post(self, *args, **kwargs):
        
        idproyecto = self.request.POST.get('idproyecto', None)
        
        self.sub_titulo ='Lista General de Solicitudes en el Proyecto'
        
        qs = SolicitudCambio.objects.filter(lineabase__fase__idproyecto_id=idproyecto)
        if qs.count() == 0 :
            return None
        
        #filtro por solicitante
        solicitante = self.request.POST.get('solicitante', '')
        if solicitante != '' :
            qs = qs.filter(solicitante=solicitante)

        #filtro por estado 
        estado = self.request.POST.get('estado', '')
        if estado != '' :
            qs = qs.filter(estado=estado)
        
        if qs.count() > 0 :
            self.title = 'Proyecto ' + qs[0].lineabase.fase.idproyecto.__unicode__()

        
        
        
        self.lista_solicitudes = qs
        return super(ListaSolicitudesPDF, self).get(self, *args, **kwargs)
    
    
class ListaSolicForm(View):
    """
    
    Vista que despliega un formulario con opciones de reporte para listar solicitudes.
    -Permite seleccionar el solicitante
    -Permite seleccionar el estado 
    
    """
    TEMPLATE = 'gestcambio/form_reportsolic.html'
    
    def get(self, request, idproyecto):
        form = ReporteSolicForm(initial={'idproyecto' :idproyecto })
        return render(self.request, self.TEMPLATE, {'form':form, 'idproyecto': idproyecto})
    