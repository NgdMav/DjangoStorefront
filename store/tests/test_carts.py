import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Cart

@pytest.fixture
def cart():
    return baker.make(Cart)

@pytest.mark.django_db
class TestCreateCart:

    def test_if_data_is_valid_returns_201(self, api_client):
        response = api_client.post('/store/carts/')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None

@pytest.mark.django_db
class TestRetrieveCart:

    def test_if_cart_exists_returns_200(self, api_client, cart):
        response = api_client.get(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_cart_not_exists_returns_404(self, api_client):
        response = api_client.get(f'/store/carts/{"some_cart"}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteCart:
    def test_delete_cart_returns_204(self, api_client, cart):
        response = api_client.delete(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
