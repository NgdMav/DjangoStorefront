import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.fixture
def make_collection():
    return baker.make(Collection)

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange

        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, auth_client):
        auth_client()

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_collection, auth_client):
        auth_client(is_staff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_collection, auth_client):
        auth_client(is_staff=True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exists_returns_200(self, api_client, make_collection):
        response = api_client.get(f'/store/collections/{make_collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': make_collection.id,
            'title': make_collection.title,
            'featured_product': make_collection.featured_product,
            'products_count': 0
        }

    def test_if_collection_not_exists_returns_404(self, api_client, make_collection):
        response = api_client.get(f'/store/collections/{make_collection.id + 1}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdateDeleteCollection:
    def test_delete_collection_returns_204(self, api_client, auth_client, make_collection):
        auth_client(is_staff=True)

        response = api_client.delete(f'/store/collections/{make_collection.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_patch_collection_returns_200(self, api_client, auth_client, make_collection):
        auth_client(is_staff=True)

        response = api_client.put(f'/store/collections/{make_collection.id}/', {'title': 'b'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'b'


