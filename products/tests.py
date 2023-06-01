from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Review
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestMyAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_request(self):
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_request(self):
        data = {'foo': 'bar'}
        response = self.client.post('/product/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.50,
            owner=self.user
        )

    def test_product_creation(self):
        p = self.product
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(p.__str__(), p.title)

    def test_product_highlighted_field(self):
        self.assertEqual(self.product.highlighted, '')


class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.50,
            owner=self.user
        )
        self.review = Review.objects.create(
            title='Test Review',
            description='This is a test review',
            grade=3.5,
            product=self.product,
            author=self.user
        )

    def test_review_creation(self):
        r = self.review
        self.assertTrue(isinstance(r, Review))
        self.assertEqual(r.__str__(), r.title)

    def test_review_highlighted_field(self):
        self.assertEqual(self.review.highlighted, '')


class ProductViewTestCase(APITestCase):
    def setUp(self):
        # Crear un usuario y un producto para usar en las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.50,
            owner=self.user
        )

    def test_list(self):
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.product.id)
        self.assertEqual(response.data[0]['title'], self.product.title)

    def test_create(self):
        url = reverse('product-list')
        data = {
            'title': 'New Product',
            'description': 'This is a new product',
            'price': 20.00
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['price'], data['price'])
        self.assertEqual(Product.objects.count(), 2)
