from django.test import TestCase
from django.contrib.auth.models import User


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
        
    
    