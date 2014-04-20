from django import template
from projectman.apps.admin.models import exist_permiso_proyecto, exist_permiso
register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.assignment_tag
def perm_proy(idusuario, idproyecto, idpermiso):
    """
    tag que verifica la existencia de un permiso general para un usuario y un proyecto.
    Setea una variable con true si existe el permiso , caso contrario false.
    
    """
    try:
        return exist_permiso_proyecto(idusuario, idproyecto, idpermiso)
    except Exception :
        return False


@register.assignment_tag
def permiso_gral(idusuario, idpermiso):
    """
    
    tag que verifica la existencia de un permiso general para un usuario.
    Setea una variable con true si existe el permiso , caso contrario false.
    
    """
    try:
        return exist_permiso(idusuario, idpermiso)
    except Exception :
        return False
