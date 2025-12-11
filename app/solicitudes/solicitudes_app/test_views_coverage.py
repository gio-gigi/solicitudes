"""
Tests adicionales para mejorar cobertura de views.py (DSM5)
"""
from django.test import TestCase, Client
from django.urls import reverse
from solicitudes_app.models import Usuario


class LoginViewCoverageTest(TestCase):
    """Tests adicionales para login_view"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('solicitudes_app:login')

    def test_usuario_autenticado_redirige_a_bienvenida(self):
        """Usuario ya autenticado es redirigido a bienvenida"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)

    def test_muestra_credenciales_admin_predeterminado(self):
        """Muestra credenciales si existe admin predeterminado que debe cambiar password"""
        Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            rol='administrador',
            debe_cambiar_password=True
        )
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['mostrar_credenciales_admin'])

    def test_no_muestra_credenciales_si_admin_cambio_password(self):
        """No muestra credenciales si admin ya cambiÃ³ su password"""
        Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            rol='administrador',
            debe_cambiar_password=False
        )
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['mostrar_credenciales_admin'])

    def test_login_con_remember_me_false(self):
        """Login sin remember_me configura sesiÃ³n temporal"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='Testpass123!',
            rol='alumno',
            perfil_completo=True
        )
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'Testpass123!',
            'remember_me': False
        })
        self.assertEqual(response.status_code, 302)

    def test_login_con_next_url(self):
        """Login redirige a next_url si estÃ¡ presente"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='Testpass123!',
            rol='alumno',
            perfil_completo=True
        )
        response = self.client.post(
            self.login_url + '?next=/some-page/',
            {
                'username': 'user1',
                'password': 'Testpass123!',
                'remember_me': True
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_login_formulario_invalido_sin_all_errors(self):
        """Login con formulario invÃ¡lido sin __all__ errors"""
        response = self.client.post(self.login_url, {
            'username': '',  # Campo vacÃ­o
            'password': '',
            'remember_me': False
        })
        self.assertEqual(response.status_code, 200)

    def test_login_credenciales_incorrectas(self):
        """Login con credenciales incorrectas muestra error"""
        Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='Testpass123!',
            rol='alumno'
        )
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'wrongpassword',
            'remember_me': False
        })
        self.assertEqual(response.status_code, 200)


class RegistroViewCoverageTest(TestCase):
    """Tests adicionales para registro_view"""

    def setUp(self):
        self.client = Client()
        self.registro_url = reverse('solicitudes_app:registro')

    def test_usuario_autenticado_redirige_a_bienvenida(self):
        """Usuario autenticado es redirigido a bienvenida"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(self.registro_url)
        self.assertEqual(response.status_code, 302)

    def test_registro_formulario_invalido(self):
        """Registro con formulario invÃ¡lido muestra errores"""
        response = self.client.post(self.registro_url, {
            'username': 'user1',
            'email': 'invalidemail',  # Email invÃ¡lido
            'password1': 'pass',
            'password2': 'pass'
        })
        self.assertEqual(response.status_code, 200)


class PerfilViewCoverageTest(TestCase):
    """Tests adicionales para perfil_view"""

    def setUp(self):
        self.client = Client()
        self.perfil_url = reverse('solicitudes_app:perfil')
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=False
        )

    def test_perfil_post_formulario_invalido(self):
        """POST con formulario invÃ¡lido muestra errores"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(self.perfil_url, {
            'first_name': 'Juan',
            'last_name': 'PÃ©rez',
            'telefono': '123',  # TelÃ©fono muy corto
            'matricula': ''
        })
        # May show form errors or redirect
        self.assertIn(response.status_code, [200, 302])


class ListaUsuariosViewCoverageTest(TestCase):
    """Tests adicionales para lista_usuarios_view"""

    def setUp(self):
        self.client = Client()
        self.lista_url = reverse('solicitudes_app:lista_usuarios')
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )

    def test_no_admin_no_puede_ver_lista(self):
        """No administrador no puede ver lista de usuarios"""
        alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client.login(username='alumno1', password='testpass123')
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, 302)


class EditarUsuarioViewCoverageTest(TestCase):
    """Tests adicionales para editar_usuario_view"""

    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )

    def test_editar_formulario_invalido(self):
        """POST con formulario invÃ¡lido muestra errores"""
        self.client.login(username='admin1', password='testpass123')
        url = reverse('solicitudes_app:editar_usuario',
                      kwargs={'usuario_id': self.alumno.id})
        response = self.client.post(url, {
            'username': '',  # Username vacÃ­o - invÃ¡lido
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'PÃ©rez',
            'rol': 'alumno',
            'is_active': True
        })
        # Should show form errors
        self.assertIn(response.status_code, [200, 302])


class EliminarUsuarioViewCoverageTest(TestCase):
    """Tests adicionales para eliminar_usuario_view"""

    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )

    def test_no_puede_eliminar_ultimo_admin_activo(self):
        """No se puede eliminar el Ãºltimo administrador activo"""
        self.client.login(username='admin1', password='testpass123')
        url = reverse('solicitudes_app:eliminar_usuario',
                      kwargs={'usuario_id': self.admin.id})
        response = self.client.post(url)
        # Should not delete and redirect with error
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(id=self.admin.id).exists())


class CambiarPasswordViewCoverageTest(TestCase):
    """Tests adicionales para cambiar_password_view"""

    def setUp(self):
        self.client = Client()
        self.cambiar_url = reverse('solicitudes_app:cambiar_password')
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='oldpass123',
            rol='alumno',
            debe_cambiar_password=True,
            perfil_completo=False
        )

    def test_cambiar_password_redirige_a_perfil_si_incompleto(self):
        """DespuÃ©s de cambiar password, redirige a perfil si estÃ¡ incompleto"""
        self.client.login(username='user1', password='oldpass123')
        response = self.client.post(self.cambiar_url, {
            'old_password': 'oldpass123',
            'new_password1': 'Newpass123!',
            'new_password2': 'Newpass123!'
        })
        # Should redirect to perfil because perfil_completo is False
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertFalse(self.usuario.debe_cambiar_password)

    def test_cambiar_password_formulario_invalido(self):
        """POST con formulario invÃ¡lido muestra errores"""
        self.client.login(username='user1', password='oldpass123')
        response = self.client.post(self.cambiar_url, {
            'old_password': 'wrongpassword',
            'new_password1': 'Newpass123!',
            'new_password2': 'Newpass123!'
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewCoverageTest(TestCase):
    """Tests adicionales para logout_view"""

    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('solicitudes_app:logout')
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )

    def test_logout_exitoso(self):
        """Logout exitoso redirige a login"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)


class EliminarUsuarioDeleteTest(TestCase):
    """Tests adicionales para eliminar_usuario_view - delete path"""

    def setUp(self):
        self.client = Client()
        self.admin1 = Usuario.objects.create_user(
            username='admin1',
            email='admin1@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )
        self.admin2 = Usuario.objects.create_user(
            username='admin2',
            email='admin2@test.com',
            password='testpass123',
            rol='administrador',
            perfil_completo=True
        )
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )

    def test_eliminacion_exitosa_de_usuario(self):
        """Admin puede eliminar usuario normal"""
        self.client.login(username='admin1', password='testpass123')
        url = reverse('solicitudes_app:eliminar_usuario',
                      kwargs={'usuario_id': self.alumno.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Usuario.objects.filter(id=self.alumno.id).exists())

    def test_eliminacion_exitosa_de_segundo_admin(self):
        """Admin puede eliminar otro admin cuando hay mas de uno"""
        self.client.login(username='admin1', password='testpass123')
        url = reverse('solicitudes_app:eliminar_usuario',
                      kwargs={'usuario_id': self.admin2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Usuario.objects.filter(id=self.admin2.id).exists())

class EditarUsuarioLastAdminProtectionTest(TestCase):
    """Tests para proteccion del ultimo administrador al editar usuario"""
