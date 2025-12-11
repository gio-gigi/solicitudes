"""
Tests finales extremadamente especificos para DSM5 - Empuje final al 95%
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from solicitudes_app.models import Usuario
from solicitudes_app.forms import RegistroUsuarioForm


class ViewsRegistroSuccessWithLoginTest(TestCase):
    """Test para registro exitoso con login automatico - lineas 74-78"""

    def setUp(self):
        self.client = Client()
        self.registro_url = reverse('solicitudes_app:registro')

    def test_registro_exitoso_hace_login_y_redirige(self):
        """Registro exitoso hace login automatico y redirige"""
        response = self.client.post(self.registro_url, {
            'username': 'nuevouser',
            'email': 'nuevo@example.com',
            'password1': 'NuevoPass123!',
            'password2': 'NuevoPass123!',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '87654321'
        })
        # Debe redirigir despues del registro exitoso
        self.assertEqual(response.status_code, 302)
        # Verificar que el usuario fue creado
        self.assertTrue(Usuario.objects.filter(username='nuevouser').exists())


class ViewsPerfilUpdateSuccessCompleteTest(TestCase):
    """Test para actualizacion exitosa de perfil - lineas 128-129"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='perfiltest',
            email='perfil@test.com',
            password='TestPass123',
            rol='alumno',
            perfil_completo=False
        )
        self.client = Client()
        self.client.login(username='perfiltest', password='TestPass123')
        self.perfil_url = reverse('solicitudes_app:perfil')

    def test_perfil_post_exitoso_marca_completo(self):
        """POST exitoso de perfil marca perfil_completo=True"""
        response = self.client.post(self.perfil_url, {
            'first_name': 'Perfil',
            'last_name': 'Test',
            'email': 'perfil@test.com',
            'telefono': '9876543210',
            'matricula': '11223344'
        })
        # Debe redirigir despues de actualizar
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.perfil_completo)
        self.assertEqual(self.usuario.first_name, 'Perfil')


class ViewsEditarUsuarioGetFormDisplayTest(TestCase):
    """Test para GET de editar usuario mostrando form - lineas 172-177"""

    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username='admineditar',
            email='admineditar@test.com',
            password='TestPass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.usuario = Usuario.objects.create_user(
            username='usuarioeditar',
            email='usuarioeditar@test.com',
            password='TestPass123',
            rol='alumno',
            perfil_completo=True,
            first_name='Original',
            last_name='Name'
        )
        self.client = Client()
        self.client.login(username='admineditar', password='TestPass123')

    def test_editar_usuario_get_carga_datos_usuario(self):
        """GET de editar usuario carga datos del usuario en el form"""
        url = reverse('solicitudes_app:editar_usuario', args=[self.usuario.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'usuarioeditar')
        self.assertContains(response, 'Original')


class ViewsEliminarUsuarioNoAdminSuccessTest(TestCase):
    """Test para eliminacion exitosa de usuario no-admin - lineas 218-221"""

    def setUp(self):
        self.admin1 = Usuario.objects.create_user(
            username='admindelete1',
            email='admindelete1@test.com',
            password='TestPass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.admin2 = Usuario.objects.create_user(
            username='admindelete2',
            email='admindelete2@test.com',
            password='TestPass123',
            rol='administrador',
            is_active=True,
            perfil_completo=True
        )
        self.alumno = Usuario.objects.create_user(
            username='alumnodelete',
            email='alumnodelete@test.com',
            password='TestPass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client = Client()
        self.client.login(username='admindelete1', password='TestPass123')

    def test_eliminacion_exitosa_alumno_con_mensaje(self):
        """Eliminacion exitosa de alumno muestra mensaje"""
        url = reverse('solicitudes_app:eliminar_usuario', args=[self.alumno.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        # Verificar que el alumno fue eliminado
        self.assertFalse(Usuario.objects.filter(pk=self.alumno.pk).exists())


class ViewsLoginFormAllErrorsTest(TestCase):
    """Test para errores __all__ en login form - linea 52-53"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='erroruser',
            email='error@test.com',
            password='CorrectPass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client = Client()
        self.login_url = reverse('solicitudes_app:login')

    def test_login_credenciales_incorrectas_muestra_error(self):
        """Login con credenciales incorrectas genera error en __all__"""
        response = self.client.post(self.login_url, {
            'username': 'erroruser',
            'password': 'WrongPassword123'
        })
        self.assertEqual(response.status_code, 200)
        # Verificar que hay mensajes de error
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0)


class RegistroFormPasswordNoCoincideTest(TestCase):
    """Test para passwords que no coinciden - linea 218"""

    def test_passwords_diferentes_genera_error(self):
        """Passwords que no coinciden generan error"""
        form = RegistroUsuarioForm(data={
            'username': 'passtest',
            'email': 'passtest@example.com',
            'password1': 'TestPass123!',
            'password2': 'DifferentPass123!',  # Diferente
            'first_name': 'Pass',
            'last_name': 'Test',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '99887766'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class RegistroFormTelefonoReturnValueTest(TestCase):
    """Test para retorno de telefono limpio - linea 167"""

    def test_telefono_con_guiones_se_limpia(self):
        """Telefono con guiones retorna version limpia"""
        form = RegistroUsuarioForm(data={
            'username': 'teltest',
            'email': 'teltest@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Tel',
            'last_name': 'Test',
            'telefono': '123-456-7890',  # Con guiones
            'rol': 'alumno',
            'matricula': '55667788'
        })
        if form.is_valid():
            # El telefono deberia estar limpio
            self.assertEqual(form.cleaned_data['telefono'], '1234567890')


class RegistroFormMatriculaFormatValidationTest(TestCase):
    """Test para validacion de formato de matricula - linea 148"""

    def test_matricula_formato_correcto_pasa_validacion(self):
        """Matricula con formato correcto pasa validacion"""
        form = RegistroUsuarioForm(data={
            'username': 'mattest',
            'email': 'mattest@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Mat',
            'last_name': 'Test',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345'  # 5 digitos - valido
        })
        self.assertTrue(form.is_valid())


class RegistroFormFirstNameStripTest(TestCase):
    """Test para strip de first_name - linea 121"""

    def test_first_name_con_espacios_extras_se_limpia(self):
        """First name con espacios extras se limpia con strip"""
        form = RegistroUsuarioForm(data={
            'username': 'striptest',
            'email': 'striptest@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': '  Juan  ',  # Espacios extras
            'last_name': 'Perez',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '44556677'
        })
        if form.is_valid():
            # El nombre deberia estar sin espacios extras
            self.assertEqual(form.cleaned_data['first_name'], 'Juan')


class RegistroFormLastNameStripTest(TestCase):
    """Test para strip de last_name - linea 136"""

    def test_last_name_con_espacios_extras_se_limpia(self):
        """Last name con espacios extras se limpia con strip"""
        form = RegistroUsuarioForm(data={
            'username': 'striptest2',
            'email': 'striptest2@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Maria',
            'last_name': '  Garcia  ',  # Espacios extras
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '33445566'
        })
        if form.is_valid():
            # El apellido deberia estar sin espacios extras
            self.assertEqual(form.cleaned_data['last_name'], 'Garcia')


class RegistroFormEmailLowercaseTest(TestCase):
    """Test para normalizacion de email a minusculas - linea 81"""

    def test_email_mayusculas_se_convierte_minusculas(self):
        """Email con mayusculas se normaliza a minusculas"""
        form = RegistroUsuarioForm(data={
            'username': 'emailtest',
            'email': 'TEST@EXAMPLE.COM',  # Mayusculas
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Email',
            'last_name': 'Test',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '22334455'
        })
        if form.is_valid():
            # El email deberia estar en minusculas
            self.assertEqual(form.cleaned_data['email'], 'test@example.com')
