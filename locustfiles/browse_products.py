from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    cart_id = None

    def on_start(self) -> None:
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

    @task(2)
    def view_products(self):
        collection_id = str(randint(1, 10))
        self.client.get(
            f'/store/products/?collection={collection_id}',
            name='/store/products')

    @task(4)
    def view_product(self):
        product_id = str(randint(1, 500))
        self.client.get(
            f'/store/products/{product_id}',
            name='/store/products/:id')

    @task(1)
    def add_to_cart(self):
        product_id = str(randint(1, 10))
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={'product_id': product_id,
                  'quantity': 1})
