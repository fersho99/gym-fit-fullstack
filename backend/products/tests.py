from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        """Envía un POST a /api/categories/ con una categoría nueva.
        Verifica que responda 201 (creada) y que ahora existan 2 categorías en la base."""
        response = self.client.post('/api/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        """Envía un GET a /api/categories/.
        Verifica que responda 200 y que la lista contenga solo la categoría creada en setUp."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='tester', email='tester@gymfit.test', password='tester123',
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00,
        )

    def test_create_product(self):
        """Envía un POST a /api/products/ con un producto nuevo, usando un usuario autenticado.
        Verifica que responda 201 y que ahora existan 2 productos en la base."""
        response = self.client.post('/api/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        """Envía un GET a /api/products/ con un usuario autenticado.
        Verifica que responda 200 y que la lista contenga solo el producto creado en setUp."""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        """Envía un PUT a /api/products/<id>/ con datos nuevos para el producto de setUp.
        Verifica que responda 200 y que el nombre guardado en la base cambie a 'Laptop Pro'."""
        response = self.client.put(f'/api/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00,
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')

    def test_delete_product(self):
        """Envía un DELETE a /api/products/<id>/ para el producto de setUp.
        Verifica que responda 204 (sin contenido) y que ya no quede ningún producto en la base."""
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        """Envía un GET a /api/products/<id>/precio-final/ con un usuario
        autenticado. Verifica que responda 200 y que la respuesta incluya
        el campo 'precio_final'."""
        response = self.client.get(f'/api/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        """Quita la autenticación del cliente y envía un GET a
        /api/products/<id>/precio-final/. Verifica que responda 401,
        comprobando que el endpoint quedó protegido con JWT."""
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)


class ProductAuthTestCase(TestCase):
    def test_list_products_without_token(self):
        """Envía un GET a /api/products/ sin ninguna autenticación.
        Verifica que responda 401, comprobando que el endpoint de productos está protegido."""
        response = APIClient().get('/api/products/')
        self.assertEqual(response.status_code, 401)
