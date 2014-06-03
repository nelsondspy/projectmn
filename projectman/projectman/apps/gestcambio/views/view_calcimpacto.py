from ...desarrollo.models import atributo_complejidad, ItemAtributosValores
 

def calc_complejidad_fase(fase_id):
    """
    
    Funcion que calcula la complejidad de una fase.
    Obtiene una queryset que todos los valores actuales de los items de la fase.
    Convierte los valores de tipo complejidad a entero.
    Suma todos los valores enteros obtenidos.
    
    """
    atr_complejidad = atributo_complejidad()
    #filtra por tipo de item, por uso actual ,por fase 
    qs_complejidades= ItemAtributosValores.objects.\
        filter(usoactual=True).\
        filter(idatributo=atr_complejidad).\
        filter(iditem__idfase_id=fase_id)
        

    suma = obt_complej_sumatoria(qs_complejidades) 
    
    return suma


def calc_complejidad_projecto(proyecto_id):
    """
    
    Funcion que calcula la complejidad del proyecto 
    Obtiene una queryset que todos los valores actuales de los items de la fase.
    Convierte los valores de tipo complejidad a entero.
    Suma todos los valores enteros obtenidos.
    
    """
    atr_complejidad = atributo_complejidad()
    #filtra por tipo de item, por uso actual ,por fase 
    qs_complejidades = ItemAtributosValores.objects.\
        filter(usoactual=True).\
        filter(idatributo=atr_complejidad).\
        filter(iditem__idfase__idproyecto_id=proyecto_id)
        
    suma = obt_complej_sumatoria(qs_complejidades)
    return suma 


def obt_complej_sumatoria(qs):
    valor_int_arr = qs.extra(select={'valor_int': "CAST(coalesce(valor, '0') AS integer)"}).values('valor_int')
    suma = 0 
    
    for valor in valor_int_arr:
        suma = suma + valor['valor_int'] 
    return suma
