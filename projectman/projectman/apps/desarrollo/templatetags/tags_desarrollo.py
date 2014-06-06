from django import template
from ..views.view_oth import get_url_edicion_actual
register = template.Library()


@register.simple_tag( takes_context = True)
def back_url_proyecto(context, nivel):
    """
    Tag que imprime un link al proyecto seleccionado actualmente.
    utiliza las variables de sesion para determinar la url.
    
    """
    url = get_url_edicion_actual(context['request'], nivel)
    return '<ol class="breadcrumb"><li><a href="' + url + '"><span class="glyphicon glyphicon-circle-arrow-left"></span> Volver al explorador</a></li></ol>'

