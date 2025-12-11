"""
Tests adicionales para cubrir lineas faltantes en views.py (DSM5)
"""
from django.test import TestCase, Client
from django.urls import reverse
from solicitudes_app.models import Usuario


class LoginViewFormErrorsTest(TestCase):
    """Tests para cubrir errores de formulario en login"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('solicitudes_app:login')

    def test_login_con_form_errors_all(self):
        """Login con errores en __all__ muestra mensaje correcto"""
        # Crear usuario para probar credenciales incorrectas
        Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )
        # Intentar login con password incorrecto
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        # Verificar que se muestra mensaje de error
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0)


class RegistroViewFormErrorsTest(TestCase):
    """Tests para cubrir errores de formulario en registro"""

    def setUp(self):
        self.client = Client()
        self.registro_url = reverse('solicitudes_app:registro')

    def test_registro_con_form_invalido_muestra_mensaje(self):
        """Registro con formulario invalido muestra mensaje de error"""
        response = self.client.post(self.registro_url, {
            'username': 'ab',  # Muy corto
            'email': 'invalidemail',  # Email invalido
            'password1': 'weak',  # Password debil
            'password2': 'different',  # No coincide
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '123',  # Muy corto
            'rol': 'alumno'
        })
        self.assertEqual(response.status_code, 200)
        # Verificar que hay errores en el formulario
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_valid())


class PerfilViewUpdateSuccessTest(TestCase):
    """Tests para actualizacion exitosa de perfil"""

    def setUp(self):
        self.client = Client()
        self.perfil_url = reverse('solicitudes_app:perfil')
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno',
            perfil_completo=False
        )
        self.client.login(username='testuser', password='TestPass123')

    def test_perfil_actualizacion_exitosa_marca_completo(self):
        """Actualizacion exitosa marca perfil como completo"""
        response = self.client.post(self.perfil_url, {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'email': 'test@test.com',
            'telefono': '1234567890',
            'matricula': '12345678'
        })
        # Deberia redirigir si es exitoso
        self.assertEqual(response.status_code, 302)
        # Verificar que el perfil se marco como completo
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.perfil_completo)


class EditarUsuarioLastAdminTest(TestCase):
    """Tests para validacion de ultimo admin en editar usuario"""

    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='TestPass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.client.login(username='admin1', password='TestPass123')

    def test_ultimo_admin_no_puede_cambiar_rol(self):
        """Ultimo admin activo no puede cambiar su rol"""
        url = reverse('solicitudes_app:editar_usuario', args=[self.admin.pk])
        response = self.client.post(url, {
            'username': 'admin1',
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'telefono': '1234567890',
            'matricula': '',
            'rol': 'control_escolar',  # Intentar cambiar rol
            'is_active': True
        })
        # No debe permitir el cambio
        self.assertEqual(response.status_code, 200)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.rol, 'administrador')

    def test_ultimo_admin_no_puede_desactivarse(self):
        """Ultimo admin activo no puede desactivarse"""
        url = reverse('solicitudes_app:editar_usuario', args=[self.admin.pk])
        response = self.client.post(url, {
            'username': 'admin1',
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'telefono': '1234567890',
            'matricula': '',
            'rol': 'administrador',
            'is_active': False  # Intentar desactivar
        })
        # No debe permitir la desactivacion
        self.assertEqual(response.status_code, 200)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)


class EliminarUsuarioLastAdminTest(TestCase):
    """Tests para validacion de ultimo admin en eliminar usuario"""

    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='TestPass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.client.login(username='admin1', password='TestPass123')

    def test_ultimo_admin_no_puede_eliminarse(self):
        """Ultimo admin activo no puede eliminarse"""
        url = reverse('solicitudes_app:eliminar_usuario', args=[self.admin.pk])
        response = self.client.post(url)
        # Debe redirigir sin eliminar
        self.assertEqual(response.status_code, 302)
        # Verificar que el admin sigue existiendo
        self.assertTrue(Usuario.objects.filter(pk=self.admin.pk).exists())


class CambiarPasswordSuccessTest(TestCase):
    """Tests para cambio de password exitoso"""

    def setUp(self):
        self.client = Client()
        self.cambiar_url = reverse('solicitudes_app:cambiar_password')

    def test_cambiar_password_con_perfil_completo_redirige_bienvenida(self):
        """Cambiar password con perfil completo redirige a bienvenida"""
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='OldPass123',
            rol='alumno',
            perfil_completo=True,
            debe_cambiar_password=True,
            first_name='Test',
            last_name='User',
            telefono='1234567890',
            matricula='12345678'
        )
        self.client.login(username='testuser', password='OldPass123')
        
        response = self.client.post(self.cambiar_url, {
            'old_password': 'OldPass123',
            'new_password1': 'NewPass123',
            'new_password2': 'NewPass123'
        })
        
        # Debe redirigir (puede ser a perfil o bienvenida)
        self.assertEqual(response.status_code, 302)
        usuario.refresh_from_db()
        self.assertFalse(usuario.debe_cambiar_password)
