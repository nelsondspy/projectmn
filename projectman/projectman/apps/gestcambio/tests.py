from django.test import TestCase
from models import ComiteProyecto
from models import Proyecto
from models import Fase
from projectman.apps.desarrollo.models import ItemTipos
from projectman.apps.desarrollo.models import Item
from django.contrib.auth.models import User
from models import CambioTipos
from models import LineaBase

"""""""""
Test de Comite de Cambio
"""""""""
class comiteTestCase(TestCase):
    usuario1 = None
    usuario2 = None
    proyectoComite1 = None
    proyectoComite2 = None
    comite1 = None
    comite2 = None
    def setUp(self):
        User.objects.create_user('nelsond', 'nelson@gmail.com', '12345')
        User.objects.create_user('arielm', 'ariel@gmail.com', '32145')
        self.proyectoComite1 = Proyecto(nombre = 'proyectoComitePrueba1', estado = Proyecto.E_NOINICIADO)
        self.proyectoComite1.save()
        self.proyectoComite2 = Proyecto(nombre = 'proyectoComitePrueba2', estado = Proyecto.E_NOINICIADO)
        self.proyectoComite2.save()
        self.comite1 = ComiteProyecto(proyecto = Proyecto.objects.get(pk=self.proyectoComite1.pk),usuario = User.objects.get(username__exact='nelsond'))
        self.comite1.save()
        self.comite2 = ComiteProyecto(proyecto = Proyecto.objects.get(pk=self.proyectoComite2.pk),usuario = User.objects.get(username__exact='arielm'))
        self.comite2.save()
       
    def test_cargar_ComiteTestCase(self):
        self.assertEqual('proyectoComitePrueba1', ((ComiteProyecto.objects.get(pk=self.comite1.id)).proyecto).nombre)
        self.assertEqual('proyectoComitePrueba2', ((ComiteProyecto.objects.get(pk=self.comite2.id)).proyecto).nombre)
        
    def test_modificar_ComiteTestCase(self):
        User.objects.create_user('fabianaR', 'fabi@gmail.com', '14325')
        usuarioM = User.objects.get(username__exact='fabianaR')
        comitep = ComiteProyecto.objects.get(pk=self.comite1.pk)
        comitep.usuario = usuarioM
        comitep.save()
        self.assertEqual(usuarioM,(ComiteProyecto.objects.get(pk=self.comite1.id).usuario))
        
    def test_eliminar_ComiteTestCase(self):
        cant_objetos = ComiteProyecto.objects.all().count()
        ComiteProyecto.objects.get(pk=self.comite1.pk).delete()
        ComiteProyecto.objects.get(pk=self.comite2.pk).delete()
        self.assertEqual(ComiteProyecto.objects.all().count(), cant_objetos - 2)
        
class cambioTipoTestCase(TestCase):
    
    cambioTipo1 = None
    cambioTipo2 = None
    def setUp(self):
        self.cambioTipo1 = CambioTipos(nombre = 'cambioTipoPrueba1')
        self.cambioTipo1.save()
        self.cambioTipo2 = CambioTipos(nombre = 'cambioTipoPrueba2')
        self.cambioTipo2.save()
        
    def test_cargar_CambioTipoTestCase(self):
        self.assertEqual('cambioTipoPrueba1', (CambioTipos.objects.get(pk=self.cambioTipo1.idtipocambio).nombre))
        self.assertEqual('cambioTipoPrueba2', (CambioTipos.objects.get(pk=self.cambioTipo2.idtipocambio).nombre))
        
    def test_modificar_cambioTipo(self):
        nombreM = 'nombreModificado'
        cambioTipo3 = CambioTipos.objects.get(pk=self.cambioTipo1.idtipocambio)
        cambioTipo3.nombre = nombreM
        cambioTipo3.save()
        self.assertEqual(nombreM, CambioTipos.objects.get(pk=self.cambioTipo1.idtipocambio).nombre)
        
    def test_eliminarcambioTipo(self):
        cant_objetos = CambioTipos.objects.all().count()
        CambioTipos.objects.get(pk=self.cambioTipo1.idtipocambio).delete()
        CambioTipos.objects.get(pk=self.cambioTipo2.idtipocambio).delete()
        self.assertEqual(CambioTipos.objects.all().count(),cant_objetos - 2)

class lineaBaseTestCase(TestCase):
    itemTipo1 = None
    item1 = None
    item2 = None
    proyecto1 = None
    fase1 = None
    fase2 = None
    LineaBasePrueba=None
    def setUp(self):
        self.proyecto1 = Proyecto(nombre = 'proyectoPrueba1', estado = Proyecto.E_NOINICIADO)
        self.proyecto1.save()
        self.fase1 = Fase(nombre = 'fasePrueba1', estado = Fase.E_INICIAL, idproyecto = self.proyecto1)
        self.fase1.save()
        self.fase2 = Fase(nombre = 'fasePrueba2', estado = Fase.E_INICIAL, idproyecto = self.proyecto1)
        self.fase2.save()
        self.itemTipo1 = ItemTipos(nombre = 'itemTipo1Prueba1', es_supertipo = 0,idfase = self.fase1)
        self.itemTipo1.save()
        self.item1 = Item(numero = 1,nombre = 'itemPrueba1',descripcion = 'esta es una prueba para lb del item1',estado = Item.E_DESAPROBADO,version = 1,idfase = self.fase1,idtipoitem = self.itemTipo1)
        self.item1.save()
        self.item2 = Item(numero = 1,nombre = 'itemPrueba2',descripcion = 'esta es una prueba para lb del item2',estado = Item.E_DESAPROBADO,version = 1,idfase = self.fase1,idtipoitem = self.itemTipo1)
        self.item2.save()
        
        self.LineaBasePrueba = LineaBase()
        self.LineaBasePrueba.fase = self.fase1
        self.LineaBasePrueba.descripcion = "linea base de prueba "
        self.LineaBasePrueba.save()
        self.LineaBasePrueba.items.add(self.item1)
        self.LineaBasePrueba.items.add(self.item2)
        self.LineaBasePrueba.save()
        
    def test_CargarLineaBaseTest(self):
        
        self.assertEqual('fasePrueba1', ((LineaBase.objects.get(pk=self.LineaBasePrueba.idlineabase)).fase).nombre)
        
