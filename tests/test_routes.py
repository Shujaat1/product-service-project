"""
TestProduct API Service Test Suite
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/products"


class TestProductService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        pass

    def setUp(self):
        """Runs before each test"""
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_read_a_product(self):
        """It should Read a single Product"""
        # Create a product to read
        test_product = self._create_products(1)[0]
        
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_update_product(self):
        """It should Update an existing Product"""
        # Create a Product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, 201)
        
        # Update the product
        new_product = response.get_json()
        new_product["description"] = "Updated description"
        
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, 200)
        
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "Updated description")

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 204)
        
        # Make sure it is deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, 404)

    def test_list_all_products(self):
        """It should Get a list of all Products"""
        self._create_products(5)
        
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(10)
        test_name = products[0].name
        name_products = [product for product in products if product.name == test_name]
        
        response = self.client.get(BASE_URL, query_string=f"name={test_name}")
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), len(name_products))
        
        # Check that all products have the correct name
        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_list_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)
        test_category = products[0].category
        category_products = [product for product in products if product.category == test_category]
        
        response = self.client.get(BASE_URL, query_string=f"category={test_category}")
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), len(category_products))
        
        # Check that all products have the correct category
        for product in data:
            self.assertEqual(product["category"], test_category)

    def test_list_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(10)
        available_products = [product for product in products if product.available is True]
        
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), len(available_products))
        
        # Check that all products are available
        for product in data:
            self.assertEqual(product["available"], True)

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, 201)
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products