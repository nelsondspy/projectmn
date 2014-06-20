# -*- coding: utf-8 -*-

from easy_pdf.views import PDFTemplateView

from datetime import date
from ..models import Item 
from ...desarrollo.models import atributo_complejidad
from ...admin.models import Proyecto
from django.shortcuts import get_object_or_404

class ProyectoInformePDF(PDFTemplateView):
    """
    
    """
    template_name = "desarrollo/rpt_lista_detalleproyecto.html"
    title = u'Lista de ítems del proyecto '
    sub_titulo = 'l'
    lista_items = None
    
    #idatributo_comlejidad #idproyecto
    
    sql_items = "SELECT i.*,f.nombre as fase_nombre , \
    (SELECT nombre FROM desarrollo_item where iditem = \
  (SELECT origen_id from desarrollo_itemrelacion as rel WHERE destino_id = i.iditem AND estado = 'ACT' LIMIT 1 )\
  ) as padre,\
  ( select valor from desarrollo_itematributosvalores as v\
    WHERE v.usoactual = TRUE AND idatributo_id = %s AND v.iditem_id = i.iditem  ) as complejidad \
FROM desarrollo_item as i \
INNER JOIN admin_fase as f ON f.idfase = i.idfase_id \
WHERE f.idproyecto_id = %s and i.estado != 'ELI' ORDER BY i.idfase_id ; "
    
    def get_context_data(self, **kwargs):
        self.set_datosconsulta()
        return super(ProyectoInformePDF, self).get_context_data(
            pagesize="A4",
            title=self.title,
            sub_titulo=self.sub_titulo, 
            fecha=date.today(),
            lista_items=self.lista_items
        )
    
    def set_datosconsulta(self):
        idproyecto = self.kwargs['idproyecto']
        proyecto = get_object_or_404(Proyecto, pk=idproyecto)
        self.title = self.title + proyecto.nombre
        self.sub_titulo = proyecto.descripcion
        atr_complejidad = atributo_complejidad()
        id_complej =  atr_complejidad[0].pk if atr_complejidad.count()> 0 else 1

        self.lista_items = Item.objects.raw(self.sql_items, [id_complej, idproyecto])
        
    
