from django.test import TestCase
from django.core.exceptions import ValidationError
from tipo_solicitudes.models import TipoSolicitud
from tipo_solicitudes.forms import FormTipoSolicitud


class TestFromTipoSolicitud(TestCase):

    def test_informacion_valida(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social'
        }
        form = FormTipoSolicitud(data)
        self.assertTrue(form.is_valid())

    def test_nombre_es_requerido(self):
        data = {
            'nombre': '',
            'descripcion': 'Constancia para servicio social'
        }
        form = FormTipoSolicitud(data)
        self.assertFalse(form.is_valid())

    def test_descripcion_es_requerido(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': ''
        }
        form = FormTipoSolicitud(data)
        self.assertFalse(form.is_valid())

    def test_nombre_es_requerido_mensaje(self):
        data = {
            'nombre': '',
            'descripcion': 'Constancia para servicio social'
        }
        form = FormTipoSolicitud(data)
        self.assertEqual(form.errors['nombre'][0], 'Este campo es obligatorio.')

    def test_guarda_constancia(self):
        data = {
            'nombre': 'Constancia',
            'descripcion': 'Constancia para servicio social'
        }
        form = FormTipoSolicitud(data)
        # form.is_valid()
        tipo_solicitud = form.save()

        self.assertEqual(tipo_solicitud.nombre, TipoSolicitud.objects.first().nombre)