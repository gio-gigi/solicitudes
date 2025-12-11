"""
Tests adicionales para mejorar cobertura de forms.py (DSM5)
"""
from django.test import TestCase
from solicitudes_app.forms import (
    RegistroUsuarioForm,
    ActualizarPerfilForm,
    GestionarUsuarioForm
)
from solicitudes_app.models import Usuario


class RegistroUsuarioFormCoverageTest(TestCase):
    """Tests adicionales para RegistroUsuarioForm"""

    def test_validacion_email_formato_invalido(self):
        """Email con formato inválido debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'user1',
            'email': 'emailinvalido',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_email_duplicado(self):
        """Email duplicado debe fallar"""
        Usuario.objects.create_user(
            username='existing',
            email='existing@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = RegistroUsuarioForm(data={
            'username': 'newuser',
            'email': 'existing@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_username_muy_corto(self):
        """Username con menos de 4 caracteres debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'usr',
            'email': 'user@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_validacion_username_caracteres_invalidos(self):
        """Username con caracteres no permitidos debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'user@name',
            'email': 'user@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_validacion_username_duplicado(self):
        """Username duplicado debe fallar"""
        Usuario.objects.create_user(
            username='existing',
            email='existing@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = RegistroUsuarioForm(data={
            'username': 'existing',
            'email': 'new@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_validacion_matricula_requerida_para_alumno(self):
        """Alumno debe tener matrícula"""
        form = RegistroUsuarioForm(data={
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_validacion_matricula_formato_invalido(self):
        """Matrícula con formato inválido debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': 'ABC',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_validacion_matricula_duplicada(self):
        """Matrícula duplicada debe fallar"""
        Usuario.objects.create_user(
            username='alumno1',
            email='alumno1@test.com',
            password='testpass123',
            rol='alumno',
            matricula='12345'
        )
        form = RegistroUsuarioForm(data={
            'username': 'alumno2',
            'email': 'alumno2@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_validacion_telefono_formato_invalido(self):
        """Teléfono con formato inválido debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'telefono': '123abc',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_password_sin_mayuscula(self):
        """Password sin mayúscula debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_validacion_password_sin_numero(self):
        """Password sin número debe fallar"""
        form = RegistroUsuarioForm(data={
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpassword!',
            'password2': 'Testpassword!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)


class ActualizarPerfilFormCoverageTest(TestCase):
    """Tests adicionales para ActualizarPerfilForm"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )

    def test_validacion_first_name_caracteres_invalidos(self):
        """Nombre con caracteres inválidos debe fallar"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan123',
                'last_name': 'Pérez',
                'email': 'user@test.com'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_validacion_last_name_caracteres_invalidos(self):
        """Apellido con caracteres inválidos debe fallar"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan',
                'last_name': 'Pérez123',
                'email': 'user@test.com'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_validacion_email_duplicado(self):
        """Email duplicado debe fallar"""
        Usuario.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'otro@test.com'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_telefono_formato_invalido(self):
        """Teléfono con formato inválido debe fallar"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'user@test.com',
                'telefono': '123'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_matricula_formato_invalido(self):
        """Matrícula con formato inválido debe fallar"""
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'user@test.com',
                'matricula': 'ABC'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_validacion_matricula_duplicada(self):
        """Matrícula duplicada debe fallar"""
        Usuario.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123',
            rol='alumno',
            matricula='12345'
        )
        form = ActualizarPerfilForm(
            data={
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'user@test.com',
                'matricula': '12345'
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)


class GestionarUsuarioFormCoverageTest(TestCase):
    """Tests adicionales para GestionarUsuarioForm"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )

    def test_validacion_username_duplicado(self):
        """Username duplicado debe fallar"""
        Usuario.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = GestionarUsuarioForm(
            data={
                'username': 'otro',
                'email': 'user@test.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_validacion_email_duplicado(self):
        """Email duplicado debe fallar"""
        Usuario.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = GestionarUsuarioForm(
            data={
                'username': 'user1',
                'email': 'otro@test.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'rol': 'alumno',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_matricula_duplicada(self):
        """Matrícula duplicada debe fallar"""
        Usuario.objects.create_user(
            username='otro',
            email='otro@test.com',
            password='testpass123',
            rol='alumno',
            matricula='12345'
        )
        form = GestionarUsuarioForm(
            data={
                'username': 'user1',
                'email': 'user@test.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'rol': 'alumno',
                'matricula': '12345',
                'is_active': True
            },
            instance=self.usuario
        )
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)
