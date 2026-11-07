from unittest.mock import patch

from django.test import TestCase
from requests.exceptions import ConnectTimeout
from rest_framework.test import APIClient

from countries.services import PAIS_NO_ENCONTRADO
from users.models import User

URL = '/api/v1/soap/country/mx/'


class FakeServicio:
    def __init__(self, nombre='Mexico'):
        self.nombre = nombre

    def CountryName(self, codigo):
        return self.nombre

    def CapitalCity(self, codigo):
        return 'Mexico City'

    def CountryCurrency(self, codigo):
        return {'sISOCode': 'MXN', 'sName': 'Pesos'}

    def CountryIntPhoneCode(self, codigo):
        return '52'

    def CountryFlag(self, codigo):
        return 'http://example.test/mx.jpg'


class FakeCliente:
    def __init__(self, servicio):
        self.service = servicio


class PaisSoapTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(User.objects.create_user(
            username='socio', email='socio@gymfit.test', password='Socio-Gym-2026!',
        ))

    def test_sin_token_responde_401(self):
        self.assertEqual(APIClient().get(URL).status_code, 401)

    @patch('countries.services.obtener_cliente', return_value=FakeCliente(FakeServicio()))
    def test_devuelve_los_datos_del_pais(self, _):
        respuesta = self.client.get(URL)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['codigo'], 'MX')
        self.assertEqual(respuesta.data['capital'], 'Mexico City')
        self.assertEqual(respuesta.data['moneda'], {'codigo': 'MXN', 'nombre': 'Pesos'})

    @patch('countries.services.obtener_cliente', return_value=FakeCliente(FakeServicio(PAIS_NO_ENCONTRADO)))
    def test_pais_inexistente_responde_404(self, _):
        self.assertEqual(self.client.get(URL).status_code, 404)

    @patch('countries.services.obtener_cliente', side_effect=ConnectTimeout())
    def test_servicio_caido_responde_502(self, _):
        self.assertEqual(self.client.get(URL).status_code, 502)

    def test_codigo_mal_formado_responde_404(self):
        self.assertEqual(self.client.get('/api/v1/soap/country/mexico/').status_code, 404)
