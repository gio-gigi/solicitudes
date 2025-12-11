"""
Tests adicionales para cobertura completa de forms.py (DSM5)
"""
from django.test import TestCase
from solicitudes_app.forms import RegistroUsuarioForm, ActualizarPerfilForm, GestionarUsuarioForm
from solicitudes_app.models import Usuario


class RegistroUsuarioFormLastNameValidationExtraTest(TestCase):
    """Tests para validaciones adicionales de apellido"""

    def test_last_name_con_caracteres_invalidos(self):
        """Apellido con numeros debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User123',  # Con numeros
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)


class RegistroUsuarioFormFirstNameInvalidCharsTest(TestCase):
    """Tests para validacion de caracteres invalidos en nombre"""

    def test_first_name_con_numeros(self):
        """Nombre con numeros debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test123',  # Con numeros
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)


class RegistroUsuarioFormMatriculaFormatTest(TestCase):
    """Tests para formato de matricula"""

    def test_matricula_con_letras_falla(self):
        """Matricula con letras debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': 'ABC12345'  # Con letras
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_matricula_muy_corta_falla(self):
        """Matricula con menos de 5 digitos debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '1234'  # Solo 4 digitos
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)


class RegistroUsuarioFormPasswordMinusculeTest(TestCase):
    """Tests para validacion de minuscula en password"""

    def test_password_sin_minuscula_falla(self):
        """Password sin minuscula debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TESTPASS123!',  # Sin minuscula
            'password2': 'TESTPASS123!',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)


class RegistroUsuarioFormPasswordLengthTest(TestCase):
    """Tests para validacion de longitud de password"""

    def test_password_muy_corto_falla(self):
        """Password con menos de 8 caracteres debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test1!',  # Solo 6 caracteres
            'password2': 'Test1!',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono': '1234567890',
            'rol': 'alumno',
            'matricula': '12345678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)


class ActualizarPerfilFormLastNameValidationTest(TestCase):
    """Tests para validacion de apellido en ActualizarPerfilForm"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )

    def test_last_name_con_numeros_falla(self):
        """Apellido con numeros debe fallar en actualizacion"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Test',
                'last_name': 'User123',  # Con numeros
                'email': 'test@test.com',
                'telefono': '1234567890',
                'matricula': '12345678'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)


class GestionarUsuarioFormUsernameInvalidTest(TestCase):
    """Tests para validacion de username con caracteres invalidos"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )

    def test_username_con_espacios_falla(self):
        """Username con espacios debe fallar"""
        form = GestionarUsuarioForm(
            data={
                'username': 'test user',  # Con espacio
                'email': 'test@test.com',
                'first_name': 'Test',
                'last_name': 'User',
                'telefono': '1234567890',
                'matricula': '12345678',
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class GestionarUsuarioFormFirstNameInvalidTest(TestCase):
    """Tests para validacion de first_name con caracteres invalidos"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )

    def test_first_name_con_numeros_falla(self):
        """First name con numeros debe fallar en GestionarUsuarioForm"""
        form = GestionarUsuarioForm(
            data={
                'username': 'testuser',
                'email': 'test@test.com',
                'first_name': 'Test123',  # Con numeros
                'last_name': 'User',
                'telefono': '1234567890',
                'matricula': '12345678',
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)


class GestionarUsuarioFormTelefonoInvalidTest(TestCase):
    """Tests para validacion de telefono con formato invalido"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )

    def test_telefono_con_letras_falla(self):
        """Telefono con letras debe fallar"""
        form = GestionarUsuarioForm(
            data={
                'username': 'testuser',
                'email': 'test@test.com',
                'first_name': 'Test',
                'last_name': 'User',
                'telefono': '123456789A',  # Con letra
                'matricula': '12345678',
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)


class GestionarUsuarioFormMatriculaInvalidTest(TestCase):
    """Tests para validacion de matricula con formato invalido"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123',
            rol='alumno'
        )

    def test_matricula_muy_larga_falla(self):
        """Matricula con mas de 8 digitos debe fallar"""
        form = GestionarUsuarioForm(
            data={
                'username': 'testuser',
                'email': 'test@test.com',
                'first_name': 'Test',
                'last_name': 'User',
                'telefono': '1234567890',
                'matricula': '123456789',  # 9 digitos
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)
