from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User

USERS_URL = '/api/v1/users/'
ME_URL = '/api/v1/auth/me/'
TOKEN_URL = '/api/v1/auth/token/'
PASSWORD_ADMIN = 'Admin-Gym-2026!'
PASSWORD_SOCIO = 'Socio-Gym-2026!'


class UserApiTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@gymfit.test', password=PASSWORD_ADMIN,
        )
        self.socio = User.objects.create_user(
            username='socio', email='socio@gymfit.test', password=PASSWORD_SOCIO, telefono='4771234567',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def login(self, email, password):
        return APIClient().post(TOKEN_URL, {'email': email, 'password': password}, format='json')

    def test_password_no_aparece_en_ninguna_respuesta(self):
        """Lista, detalle, creacion, edicion y /auth/me/ no devuelven el hash."""
        respuestas = [
            self.client.get(USERS_URL).data[0],
            self.client.get(f'{USERS_URL}{self.socio.id}/').data,
            self.client.post(USERS_URL, {
                'username': 'nuevo', 'email': 'nuevo@gymfit.test', 'password': PASSWORD_SOCIO,
            }, format='json').data,
            self.client.patch(f'{USERS_URL}{self.socio.id}/', {'first_name': 'Ana'}, format='json').data,
            self.client.get(ME_URL).data,
        ]
        for datos in respuestas:
            self.assertIn('email', datos)
            self.assertNotIn('password', datos)

    def test_patch_sin_password_no_cambia_la_contrasena(self):
        hash_original = self.socio.password
        respuesta = self.client.patch(f'{USERS_URL}{self.socio.id}/', {'telefono': '4770000000'}, format='json')
        self.assertEqual(respuesta.status_code, 200)
        self.socio.refresh_from_db()
        self.assertEqual(self.socio.telefono, '4770000000')
        self.assertEqual(self.socio.password, hash_original)
        self.assertEqual(self.login('socio@gymfit.test', PASSWORD_SOCIO).status_code, 200)
        self.assertEqual(self.login('socio@gymfit.test', PASSWORD_ADMIN).status_code, 401)

    def test_put_sin_password_no_cambia_la_contrasena(self):
        hash_original = self.socio.password
        respuesta = self.client.put(f'{USERS_URL}{self.socio.id}/', {
            'username': 'socio', 'email': 'socio@gymfit.test', 'first_name': 'Ana',
        }, format='json')
        self.assertEqual(respuesta.status_code, 200)
        self.socio.refresh_from_db()
        self.assertEqual(self.socio.password, hash_original)

    def test_patch_con_password_si_la_cambia_y_la_guarda_hasheada(self):
        nueva = 'Nueva-Clave-2026!'
        respuesta = self.client.patch(f'{USERS_URL}{self.socio.id}/', {'password': nueva}, format='json')
        self.assertEqual(respuesta.status_code, 200)
        self.socio.refresh_from_db()
        self.assertNotEqual(self.socio.password, nueva)
        self.assertTrue(self.socio.check_password(nueva))

    def test_crear_usuario_guarda_el_hash_y_el_telefono(self):
        respuesta = self.client.post(USERS_URL, {
            'username': 'nuevo', 'email': 'nuevo@gymfit.test',
            'password': PASSWORD_SOCIO, 'telefono': '+524771112233',
        }, format='json')
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.data['telefono'], '+524771112233')
        nuevo = User.objects.get(email='nuevo@gymfit.test')
        self.assertTrue(nuevo.check_password(PASSWORD_SOCIO))

    def test_crear_usuario_sin_password_falla(self):
        respuesta = self.client.post(USERS_URL, {'username': 'nuevo', 'email': 'nuevo@gymfit.test'}, format='json')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('password', respuesta.data)

    def test_password_debil_se_rechaza(self):
        respuesta = self.client.patch(f'{USERS_URL}{self.socio.id}/', {'password': '123'}, format='json')
        self.assertEqual(respuesta.status_code, 400)
        self.socio.refresh_from_db()
        self.assertTrue(self.socio.check_password(PASSWORD_SOCIO))

    def test_telefono_invalido_se_rechaza(self):
        respuesta = self.client.patch(f'{USERS_URL}{self.socio.id}/', {'telefono': 'abc'}, format='json')
        self.assertEqual(respuesta.status_code, 400)

    def test_usuario_normal_no_accede_al_crud(self):
        cliente = APIClient()
        cliente.force_authenticate(user=self.socio)
        self.assertEqual(cliente.get(USERS_URL).status_code, 403)


class AuthJwtTestCase(TestCase):
    def setUp(self):
        self.socio = User.objects.create_user(
            username='socio', email='socio@gymfit.test', password=PASSWORD_SOCIO, telefono='4771234567',
        )

    def test_login_con_email_y_consulta_de_datos_personales(self):
        token = APIClient().post(TOKEN_URL, {
            'email': 'socio@gymfit.test', 'password': PASSWORD_SOCIO,
        }, format='json')
        self.assertEqual(token.status_code, 200)
        cliente = APIClient()
        cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {token.data['access']}")
        respuesta = cliente.get(ME_URL)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['email'], 'socio@gymfit.test')
        self.assertEqual(respuesta.data['telefono'], '4771234567')
        self.assertNotIn('password', respuesta.data)

    def test_datos_personales_sin_token_responde_401(self):
        self.assertEqual(APIClient().get(ME_URL).status_code, 401)

    def test_tiempo_de_vida_del_token_de_acceso(self):
        self.assertEqual(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], timedelta(minutes=30))


class RegisterTestCase(TestCase):
    URL = '/api/v1/auth/register/'
    DATOS = {
        'username': 'nuevo', 'email': 'nuevo@gymfit.test',
        'password': PASSWORD_SOCIO, 'telefono': '4771234567',
    }

    def test_registro_crea_usuario_sin_devolver_password_y_permite_login(self):
        respuesta = APIClient().post(self.URL, self.DATOS, format='json')
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.data['email'], 'nuevo@gymfit.test')
        self.assertNotIn('password', respuesta.data)
        login = APIClient().post(TOKEN_URL, {
            'email': 'nuevo@gymfit.test', 'password': PASSWORD_SOCIO,
        }, format='json')
        self.assertEqual(login.status_code, 200)

    def test_registro_no_permite_darse_permisos(self):
        datos = {**self.DATOS, 'is_staff': True, 'is_superuser': True}
        self.assertEqual(APIClient().post(self.URL, datos, format='json').status_code, 201)
        nuevo = User.objects.get(email='nuevo@gymfit.test')
        self.assertFalse(nuevo.is_staff)
        self.assertFalse(nuevo.is_superuser)

    def test_registro_rechaza_password_debil(self):
        respuesta = APIClient().post(self.URL, {**self.DATOS, 'password': '12345678'}, format='json')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('password', respuesta.data)

    def test_registro_rechaza_email_repetido(self):
        APIClient().post(self.URL, self.DATOS, format='json')
        respuesta = APIClient().post(self.URL, {**self.DATOS, 'username': 'otro'}, format='json')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('email', respuesta.data)


class SwaggerTestCase(TestCase):
    def test_swagger_muestra_titulo_endpoints_y_telefono(self):
        respuesta = APIClient().get('/swagger.json')
        self.assertEqual(respuesta.status_code, 200)
        esquema = respuesta.json()
        self.assertEqual(esquema['info']['title'], 'API Gym Fit')
        self.assertIn('/v1/auth/me/', esquema['paths'])
        self.assertIn('/v1/auth/token/', esquema['paths'])
        self.assertIn('telefono', esquema['definitions']['User']['properties'])

    def test_swagger_no_documenta_password_en_las_respuestas(self):
        esquema = APIClient().get('/swagger.json').json()

        def propiedades(operacion, codigo):
            ref = operacion['responses'][codigo]['schema']
            nombre = ref.get('items', ref)['$ref'].rsplit('/', 1)[-1]
            return esquema['definitions'][nombre]['properties']

        usuarios = esquema['paths']['/v1/users/']
        detalle = esquema['paths']['/v1/users/{id}/']
        operaciones = [
            (usuarios['get'], '200'), (usuarios['post'], '201'), (detalle['get'], '200'),
            (detalle['put'], '200'), (detalle['patch'], '200'),
            (esquema['paths']['/v1/auth/me/']['get'], '200'),
        ]
        for operacion, codigo in operaciones:
            self.assertIn('telefono', propiedades(operacion, codigo))
            self.assertNotIn('password', propiedades(operacion, codigo))
        login = propiedades(esquema['paths']['/v1/auth/token/']['post'], '200')
        self.assertEqual(set(login), {'access', 'refresh'})
