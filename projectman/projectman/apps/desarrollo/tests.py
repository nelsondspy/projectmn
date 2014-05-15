from django.test import TestCase
from models import ItemTipos
from projectman.apps.admin.models import Proyecto, Fase
from models import ItemAtributos
from models import ItemAtributosValores

class ItemTiposTestCase(TestCase):
    
    item1 = None
    item2 = None
    proyecto1 = None
    fase1 = None
    def setUp(self):
        self.proyecto1 = Proyecto(nombre = 'proyectoPrueba1', estado = Proyecto.E_NOINICIADO)
        self.proyecto1.save()
        self.fase1 = Fase(nombre = 'fasePrueba1', estado = Fase.E_INICIAL, idproyecto = self.proyecto1)
        self.fase1.save()
        self.item1 = ItemTipos(nombre = 'itemPrueba1', es_supertipo = 0,idfase = self.fase1)
        self.item1.save()
        self.item2 = ItemTipos(nombre = 'itemPrueba2', es_supertipo = 0,idfase = self.fase1)
        self.item2.save()
        
    def test_cargar_ItemTiposTestCase(self):
        self.assertEqual('itemPrueba1', (ItemTipos.objects.get(pk=self.item1.idtipoitem)).nombre)
        self.assertEqual('itemPrueba2', (ItemTipos.objects.get(pk=self.item2.idtipoitem)).nombre)
        
    def test_modificar_ItemTipos(self):
        nombreItemTipo = 'itemModificado'
        itemsTipos = ItemTipos.objects.get(pk=self.item1.idtipoitem)
        itemsTipos.nombre = nombreItemTipo
        itemsTipos.save()

    def test_eliminar_TipoItem(self):
        cant_objetos_itemTipos = ItemTipos.objects.all().count()
        ItemTipos.objects.get(pk=self.item1.idtipoitem).delete()
        ItemTipos.objects.get(pk=self.item2.idtipoitem).delete()
        
        self.assertEqual(ItemTipos.objects.all().count(), cant_objetos_itemTipos-2)
        
class ItemAtributosTestCase(TestCase):
    
    itemtipo1 = None
    itemtipo2 = None
    proyecto1 = None
    fase1 = None
    itemAtributo1 = None
    itemAtributo2 = None
    def setUp(self):
        self.proyecto1 = Proyecto(nombre = 'proyectoPrueba1', estado = Proyecto.E_NOINICIADO)
        self.proyecto1.save()
        self.fase1 = Fase(nombre = 'fasePrueba1', estado = Fase.E_INICIAL, idproyecto = self.proyecto1)
        self.fase1.save()
        self.itemTipo1 = ItemTipos(nombre = 'itemPrueba1', es_supertipo = 0,idfase = self.fase1)
        self.itemTipo1.save()
        self.itemTipo2 = ItemTipos(nombre = 'itemPrueba2', es_supertipo = 0,idfase = self.fase1)
        self.itemTipo2.save()
        self.itemAtributo1 = ItemAtributos(nombre = 'atributoPrueba1',tipodato = ItemAtributos.T_CHAR,idtipoitem=self.itemTipo1)
        self.itemAtributo1.save()
        self.itemAtributo2 = ItemAtributos(nombre = 'atributoPrueba2',tipodato = ItemAtributos.T_CHAR,idtipoitem=self.itemTipo2)
        self.itemAtributo2.save()
    
    def test_cargar_itemAtributo(self):
        self.assertEqual('atributoPrueba1', (ItemAtributos.objects.get(pk=self.itemAtributo1.idatributo)).nombre)
        self.assertEqual('atributoPrueba2', (ItemAtributos.objects.get(pk=self.itemAtributo2.idatributo)).nombre)
    
    def test_modificar_itemAtributo(self):
        nombreA = 'atributoNombreMod1'
        itemAtributo = ItemAtributos.objects.get(pk=self.itemAtributo1.idatributo)
        itemAtributo.nombre = nombreA
        itemAtributo.save()
    
    def test_eliminar_itemAtributo(self):
        cant_objetos_itemAtributos = ItemAtributos.objects.all().count()
        ItemAtributos.objects.get(pk=self.itemAtributo1.idatributo).delete()
        ItemAtributos.objects.get(pk=self.itemAtributo2.idatributo).delete()
        
        self.assertEqual(ItemAtributos.objects.all().count(), cant_objetos_itemAtributos-2)
    
