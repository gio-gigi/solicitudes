from django.test import TestCase, Client
from django.urls import reverse
from solicitudes_app.models import Usuario


class EditarUsuarioLastAdminProtectionTest(TestCase):
    """Tests para proteccion del ultimo administrador al editar usuario"""

    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.client = Client()
        self.client.login(username='admin1', password='testpass123')

    def test_no_permitir_cambiar_rol_de_ultimo_admin(self):
        """No se puede cambiar el rol del ultimo admin activo"""
        url = reverse('solicitudes_app:editar_usuario', args=[self.admin.pk])
        response = self.client.post(url, {
            'username': 'admin1',
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'telefono': '1234567890',
            'matricula': '',
            'rol': 'control_escolar',
            'is_active': True
        })
        # Should prevent modification and show error
        self.assertEqual(response.status_code, 200)

    def test_no_permitir_desactivar_ultimo_admin(self):
        """No se puede desactivar el ultimo admin activo"""
        url = reverse('solicitudes_app:editar_usuario', args=[self.admin.pk])
        response = self.client.post(url, {
            'username': 'admin1',
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'telefono': '1234567890',
            'matricula': '',
            'rol': 'administrador',
            'is_active': False
        })
        # Should prevent modification and show error
        self.assertEqual(response.status_code, 200)


class LoginFormValidationErrorsTest(TestCase):
    """Tests para errores de validacion en formulario de login"""

    def setUp(self):
        self.client = Client()

    def test_error_generico_en_formulario_sin_all_errors(self):
        """Muestra error generico cuando hay problemas en el formulario"""
        response = self.client.post(reverse('solicitudes_app:login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertTrue(any('corrige los errores' in str(m) for m in messages_list))


class CambiarPasswordSuccessRedirectTest(TestCase):
    """Tests para redireccion exitosa al cambiar password"""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='Oldpass123',
            rol='alumno',
            perfil_completo=True,
            first_name='Test',
            last_name='User'
        )
        self.client = Client()
        self.client.login(username='testuser', password='Oldpass123')

    def test_redireccion_exitosa_a_bienvenida_con_perfil_completo(self):
        """Redirige a bienvenida cuando perfil completo y password cambiado"""
        url = reverse('solicitudes_app:cambiar_password')
        response = self.client.post(url, {
            'old_password': 'Oldpass123',
            'new_password1': 'Newpass123',
            'new_password2': 'Newpass123'
        })
        self.assertEqual(response.status_code, 302)
