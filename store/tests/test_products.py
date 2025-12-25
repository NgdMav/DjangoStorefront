import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Product, Collection


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.fixture
def make_product():
    collection = baker.make(Collection)
    return baker.make(Product, collection=collection)

@pytest.fixture
def get_product(make_product):
    return {
            'title': make_product.title,
            'description': '',
            'slug': make_product.slug,
            'inventory': make_product.inventory,
            'unit_price': make_product.unit_price,
            'collection': make_product.collection.id
        }

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product, get_product):
        response = create_product(get_product)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_product, auth_client, get_product):
        auth_client()

        response = create_product(get_product)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_product, auth_client):
        auth_client(is_staff=True)

        response = create_product({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_product, auth_client, get_product):
        auth_client(is_staff=True)

        response = create_product(get_product)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveProduct:

    def test_if_product_exists_returns_200(self, api_client, make_product):
        response = api_client.get(f'/store/products/{make_product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == make_product.id
        assert response.data['title'] == make_product.title

    def test_if_product_not_exists_returns_404(self, api_client, make_product):
        response = api_client.get(f'/store/products/{make_product.id + 1}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdateDeleteProduct:
    def test_delete_product_returns_204(self, api_client, auth_client, make_product):
        auth_client(is_staff=True)

        response = api_client.delete(f'/store/products/{make_product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_patch_product_returns_200(self, api_client, auth_client, make_product):
        auth_client(is_staff=True)

        response = api_client.patch(f'/store/products/{make_product.id}/', {'title': 'b'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'b'