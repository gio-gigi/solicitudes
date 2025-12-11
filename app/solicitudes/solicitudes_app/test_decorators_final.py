from django.test import TestCase, Client
from django.urls import reverse
from solicitudes_app.models import Usuario
from solicitudes_app.decorators import puede_crear_tipo_solicitud, puede_atender_solicitudes


class DecoradorCrearTipoSolicitudErrorMessagesTest(TestCase):
    """Tests para mensajes de error del decorador puede_crear_tipo_solicitud"""

    def setUp(self):
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client = Client()

    @puede_crear_tipo_solicitud
    def dummy_view(self, request):
        """Vista dummy para probar decorador"""
        from django.http import HttpResponse
        return HttpResponse('OK')

    def test_mensaje_error_sin_permisos_crear_tipo(self):
        """Muestra mensaje de error cuando usuario no tiene permisos para crear tipos"""
        self.client.login(username='alumno1', password='testpass123')
        # Necesitamos una vista real que use el decorador
        # Vamos a probar accediendo directamente a traves de la app
        from django.contrib.messages import get_messages
        response = self.client.get('/solicitudes/crear-tipo-solicitud/')
        messages = list(get_messages(response.wsgi_request))
        # Verificar que hay un mensaje de error
        self.assertTrue(any('permiso' in str(m).lower() for m in messages))


class DecoradorAtenderSolicitudesErrorMessagesTest(TestCase):
    """Tests para mensajes de error del decorador puede_atender_solicitudes"""

    def setUp(self):
        self.alumno = Usuario.objects.create_user(
            username='alumno1',
            email='alumno@test.com',
            password='testpass123',
            rol='alumno',
            perfil_completo=True
        )
        self.client = Client()

    def test_mensaje_error_sin_permisos_atender(self):
        """Muestra mensaje de error cuando usuario no tiene permisos para atender"""
        self.client.login(username='alumno1', password='testpass123')
        from django.contrib.messages import get_messages
        # Intentar acceder a vista que requiere poder atender solicitudes
        response = self.client.get('/solicitudes/atender/')
        messages = list(get_messages(response.wsgi_request))
        # Verificar mensaje de error
        self.assertTrue(any('permiso' in str(m).lower() for m in messages))
