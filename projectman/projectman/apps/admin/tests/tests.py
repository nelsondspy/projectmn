from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Proyecto
from ..models import Fase 


class UserTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user('nelsond', 'nelson@gmail.com', '12345')
        User.objects.create_user('arielm', 'ariel@gmail.com', '32145')
        User.objects.create_user('fabianar', 'fabi@gmail.com', '589752')
    
    def test_carga_usuarios(self):
        """Usuarios guardados correctamente."""
    
        self.assertEqual('nelsond', (User.objects.get(username__exact='nelsond')).username)
        self.assertEqual('fabianar', (User.objects.get(username__exact='fabianar')).username)
        
    def test_modificacion_usuarios(self):
        """Test de modificacion de usuarios"""
        email = 'arielmendez@gmail.com'
        ar =  User.objects.get(username__exact='arielm')
        ar.email = email
        ar.save()
        self.assertEqual(email, (User.objects.get(username__exact='arielm')).email)
    
    def test_eliminacion_usuarios(self):
        """Test de eliminacion de usuarios"""
        cant_objetos = User.objects.all().count()
        
        User.objects.get(username__exact='arielm').delete()
        User.objects.get(username__exact='nelsond').delete()
        User.objects.get(username__exact='fabianar').delete()
        self.assertEqual(User.objects.all().count(), cant_objetos - 3)
        
class ProyectoTestCase(TestCase):
    proyectop1 = None
    proyectop2 = None
    def setUp(self):
            self.proyectop1 = Proyecto(nombre = 'proyectoPrueba1', estado = Proyecto.E_NOINICIADO)
            self.proyectop1.save()
            self.proyectop2 = Proyecto(nombre = 'proyectoPrueba2', estado = Proyecto.E_NOINICIADO)
            self.proyectop2.save()
    
    def test_cargar_proyecto(self):
        self.assertEqual('proyectoPrueba1', (Proyecto.objects.get(pk=self.proyectop1.pk)).nombre)
        self.assertEqual('proyectoPrueba2', (Proyecto.objects.get(pk=self.proyectop2.pk)).nombre)
    
    def test_modificar_proyecto(self):
        nombreM = 'nombreModificado'
        proyectop3 = Proyecto.objects.get(pk=self.proyectop1.pk)
        proyectop3.nombre = nombreM
        proyectop3.save()
        self.assertEqual(nombreM, Proyecto.objects.get(pk=self.proyectop1.pk).nombre)
    
    def test_eliminar_proyecto(self):
        cant_objetos = Proyecto.objects.all().count()
        
        Proyecto.objects.get(pk=self.proyectop1.pk).delete()
        Proyecto.objects.get(pk=self.proyectop2.pk).delete()
        self.assertEqual(Proyecto.objects.all().count(), cant_objetos - 2)
        
class FaseTestCase(TestCase):
    fase1 = None
    fase2 = None
    proyectop1 = None
    proyectop2 = None
    def setUp(self):
        self.proyectop1 = Proyecto(nombre = 'proyectoPrueba1', estado = Proyecto.E_NOINICIADO)
        self.proyectop1.save()
        self.proyectop2 = Proyecto(nombre = 'proyectoPrueba2', estado = Proyecto.E_NOINICIADO)
        self.proyectop2.save()
        self.fase1 = Fase(nombre = 'fasePrueba1', estado = Fase.E_INICIAL, idproyecto = self.proyectop1)
        self.fase1.save()
        self.fase2 = Fase(nombre = 'fasePrueba2', estado = Fase.E_INICIAL, idproyecto = self.proyectop2)
        self.fase2.save()
    
    def test_cargar_fase(self):
        self.assertEqual('fasePrueba1', (Fase.objects.get(pk=self.fase1.idfase)).nombre)
        self.assertEqual('fasePrueba2', (Fase.objects.get(pk=self.fase2.idfase)).nombre)
    
    def test_modificar_fase(self):
        nombreF = 'faseModificada'
        fase = Fase.objects.get(pk=self.fase1.idfase)
        fase.nombre = nombreF
        fase.save()
        self.assertEqual(nombreF, Fase.objects.get(pk=self.fase1.idfase).nombre)
    
    def test_eliminar_fase(self):
        cant_objetos_fase = Fase.objects.all().count()
        Fase.objects.get(pk=self.fase1.idfase).delete()
        Fase.objects.get(pk=self.fase2.idfase).delete()
        
        self.assertEqual(Fase.objects.all().count(), cant_objetos_fase-2)
    