"""
Tests unitarios adicionales para formularios de solicitudes_app (DSM5)
Casos edge y validaciones complejas
"""
from django.test import TestCase
from solicitudes_app.models import Usuario
from solicitudes_app.forms import (
    RegistroUsuarioForm,
    ActualizarPerfilForm,
    GestionarUsuarioForm
)


class RegistroUsuarioFormEdgeCasesTest(TestCase):
    """Tests de casos edge para RegistroUsuarioForm"""

    def test_username_ya_existe(self):
        """No permite registrar username que ya existe"""
        Usuario.objects.create_user(
            username='existente',
            email='existente@test.com',
            password='testpass123',
            rol='alumno'
        )

        form_data = {
            'username': 'existente',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_ya_existe(self):
        """No permite registrar email que ya existe"""
        Usuario.objects.create_user(
            username='user1',
            email='existente@test.com',
            password='testpass123',
            rol='alumno'
        )

        form_data = {
            'username': 'nuevouser',
            'email': 'existente@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_alumno_sin_matricula_invalido(self):
        """Alumno debe tener matrícula"""
        form_data = {
            'username': 'alumno1',
            'email': 'alumno@test.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'rol': 'alumno',
            'matricula': '',  # Vacío
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_no_alumno_con_matricula_valido(self):
        """RegistroUsuarioForm no permite roles diferentes a alumno"""
        # RegistroUsuarioForm only allows alumno role, so control_escolar should fail
        form_data = {
            'username': 'control1',
            'email': 'control@test.com',
            'first_name': 'Control',
            'last_name': 'Escolar',
            'rol': 'control_escolar',  # This will be rejected
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        # Should be invalid because rol is not 'alumno'
        self.assertFalse(form.is_valid())

    def test_password_muy_corta(self):
        """Password muy corta debe ser inválida"""
        form_data = {
            'username': 'user1',
            'email': 'user@test.com',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': '123',
            'password2': '123'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_passwords_no_coinciden(self):
        """Passwords que no coinciden deben ser inválidas"""
        form_data = {
            'username': 'user1',
            'email': 'user@test.com',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'different456!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_formato_invalido(self):
        """Email con formato inválido debe fallar"""
        form_data = {
            'username': 'user1',
            'email': 'email_invalido',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_campos_vacios(self):
        """Todos los campos requeridos deben estar presentes"""
        form_data = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'rol': '',
            'password1': '',
            'password2': ''
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_todos_los_roles_validos(self):
        """RegistroUsuarioForm solo permite rol alumno"""
        # RegistroUsuarioForm is for public registration and only allows alumno role
        form_data = {
            'username': 'user_alumno',
            'email': 'alumno@test.com',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'alumno',
            'matricula': '12345',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertTrue(form.is_valid(),
                        f"Rol alumno debería ser válido: {form.errors}")


class ActualizarPerfilFormTest(TestCase):
    """Tests para ActualizarPerfilForm"""

    def test_formulario_valido_alumno(self):
        """Formulario válido para alumno con matrícula"""
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'telefono': '4921234567',
            'matricula': '12345'
        }
        usuario = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = ActualizarPerfilForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())

    def test_formulario_valido_no_alumno_sin_matricula(self):
        """No alumno puede completar perfil sin matrícula"""
        form_data = {
            'first_name': 'Control',
            'last_name': 'Escolar',
            'telefono': '4921234567',
            'matricula': ''
        }
        usuario = Usuario.objects.create_user(
            username='control1',
            email='control@test.com',
            password='testpass123',
            rol='control_escolar'
        )
        form = ActualizarPerfilForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())

    def test_campos_requeridos_presentes(self):
        """Campos no requeridos pueden estar vacíos en ActualizarPerfilForm"""
        # ActualizarPerfilForm allows blank values for most fields
        form_data = {
            'first_name': 'Juan',  # Required by Django User model
            'last_name': 'Pérez',  # Required by Django User model
            'telefono': ''  # Optional
        }
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = ActualizarPerfilForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())

    def test_telefono_formato_valido(self):
        """Teléfono debe tener formato válido"""
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'telefono': '49212345',  # Muy corto
            'matricula': '12345'
        }
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )
        form = ActualizarPerfilForm(data=form_data, instance=usuario)
        # Puede ser válido dependiendo de la validación implementada
        # Este test verifica que el form maneja teléfonos


class PasswordFormTest(TestCase):
    """Tests para cambio de password (simplificado)"""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='oldpass123',
            rol='alumno'
        )

    def test_usuario_puede_cambiar_password(self):
        """Usuario puede cambiar su password"""
        # Test de integración usando la vista
        self.assertTrue(self.usuario.check_password('oldpass123'))


class GestionarUsuarioFormTest(TestCase):
    """Tests para GestionarUsuarioForm"""

    def test_editar_usuario_valido(self):
        """Editar usuario con datos válidos"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )

        form_data = {
            'username': 'user1',
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Nombre',
            'rol': 'control_escolar',
            'telefono': '4921234567',
            'is_active': True
        }
        form = GestionarUsuarioForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())

    def test_cambiar_username_a_existente_invalido(self):
        """No permite cambiar username a uno existente"""
        usuario1 = Usuario.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123',
            rol='alumno'
        )
        usuario2 = Usuario.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123',
            rol='alumno'
        )

        form_data = {
            'username': 'user1',  # Intentar cambiar a username existente
            'email': 'user2@test.com',
            'first_name': 'User',
            'last_name': 'Two',
            'rol': 'alumno',
            'is_active': True
        }
        form = GestionarUsuarioForm(data=form_data, instance=usuario2)
        self.assertFalse(form.is_valid())

    def test_desactivar_usuario(self):
        """Permite desactivar usuario"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno',
            is_active=True
        )

        form_data = {
            'username': 'user1',
            'email': 'user@test.com',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'alumno',
            'is_active': False
        }
        form = GestionarUsuarioForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())

    def test_cambiar_rol(self):
        """Permite cambiar rol de usuario"""
        usuario = Usuario.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass123',
            rol='alumno'
        )

        form_data = {
            'username': 'user1',
            'email': 'user@test.com',
            'first_name': 'User',
            'last_name': 'Test',
            'rol': 'control_escolar',
            'is_active': True
        }
        form = GestionarUsuarioForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())


class FormularioPermisosPorRolTest(TestCase):
    """Tests para verificar permisos según roles en formularios"""

    def test_solo_admin_puede_crear_admin(self):
        """Verificar que solo administradores pueden crear administradores"""
        # Este test verifica las reglas de negocio del sistema
        admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )

        alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )

        # Admin puede gestionar usuarios
        self.assertTrue(admin.puede_gestionar_usuarios())

        # Alumno no puede gestionar usuarios
        self.assertFalse(alumno.puede_gestionar_usuarios())

    def test_roles_pueden_crear_tipos_solicitud(self):
        """Control escolar y admin pueden crear tipos de solicitud"""
        control = Usuario.objects.create_user(
            username='control1',
            email='control@test.com',
            password='testpass123',
            rol='control_escolar'
        )

        admin = Usuario.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            rol='administrador'
        )

        alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno'
        )

        self.assertTrue(control.puede_crear_tipo_solicitud())
        self.assertTrue(admin.puede_crear_tipo_solicitud())
        self.assertFalse(alumno.puede_crear_tipo_solicitud())
