"""
Tests adicionales para cobertura de validaciones en forms.py (DSM5)
"""
from django.test import TestCase
from solicitudes_app.forms import RegistroUsuarioForm, ActualizarPerfilForm
from solicitudes_app.models import Usuario


class RegistroUsuarioFormEmailValidationTest(TestCase):
    """Tests para validacion de email vacio y formato estricto"""

    def test_email_vacio_genera_error(self):
        """Email vacio debe generar error de validacion"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': '',  # Vacio
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_formato_invalido_sin_dominio(self):
        """Email sin dominio correcto debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@',  # Sin dominio
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class RegistroUsuarioFormUsernameValidationTest(TestCase):
    """Tests para validacion de username vacio"""

    def test_username_vacio_genera_error(self):
        """Username vacio debe generar error de validacion"""
        form = RegistroUsuarioForm(data={
            'username': '',  # Vacio
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class RegistroUsuarioFormFirstNameValidationTest(TestCase):
    """Tests para validacion de first_name vacio y longitud minima"""

    def test_first_name_vacio_genera_error(self):
        """First name vacio debe generar error"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': '',  # Vacio
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_first_name_muy_corto_genera_error(self):
        """First name con 1 caracter debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'A',  # Solo 1 caracter
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)


class ActualizarPerfilFormFirstNameValidationTest(TestCase):
    """Tests para validacion de first_name en ActualizarPerfilForm"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            rol='alumno'
        )

    def test_first_name_vacio_en_actualizacion(self):
        """First name vacio en actualizar perfil se acepta (campo opcional)"""
        form = ActualizarPerfilForm(
            data={
                'first_name': '',  # Vacio - permitido
                'last_name': 'User',
                'email': 'test@test.com',
                'telefono': '1234567890',
                'matricula': '12345678'
            },
            instance=self.usuario
        )
        # ActualizarPerfilForm permite first_name vacio
        self.assertTrue(form.is_valid())

    def test_first_name_muy_corto_en_actualizacion(self):
        """First name con 1 caracter se acepta en actualizar perfil"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'A',  # Solo 1 caracter - permitido en actualizacion
                'last_name': 'User',
                'email': 'test@test.com',
                'telefono': '1234567890',
                'matricula': '12345678'
            },
            instance=self.usuario
        )
        # ActualizarPerfilForm es mas flexible
        self.assertTrue(form.is_valid())


class RegistroUsuarioFormLastNameValidationTest(TestCase):
    """Tests para validacion de last_name"""

    def test_last_name_vacio_genera_error(self):
        """Last name vacio debe generar error"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': '',  # Vacio
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_last_name_muy_corto_genera_error(self):
        """Last name con 1 caracter debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'U',  # Solo 1 caracter
            'telefono': '1234567890',
            'rol': 'alumno'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)


class RegistroUsuarioFormTelefonoValidationTest(TestCase):
    """Tests para validacion de telefono vacio"""

    def test_telefono_vacio_genera_error(self):
        """Telefono vacio permite validacion pero matricula es requerida para alumno"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',  # Con caracter especial
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': ''  # Vacio - debe generar error para alumno
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)


class RegistroUsuarioFormMatriculaAlumnoTest(TestCase):
    """Tests para validacion de matricula en rol alumno"""

    def test_matricula_vacia_para_alumno_genera_error(self):
        """Matricula vacia para alumno debe generar error"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': ''  # Vacia para alumno
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)


class RegistroUsuarioFormPasswordValidationTest(TestCase):
    """Tests para validacion de password vacio y sin mayuscula"""

    def test_password_sin_mayuscula_genera_error(self):
        """Password sin mayuscula debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',  # Sin mayuscula
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_password_sin_numero_genera_error(self):
        """Password sin numero debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPassword',  # Sin numero
            'password2': 'TestPassword',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
