import pytest
from model_bakery import baker
from rest_framework import status

from core.models import User
from store.models import Customer


@pytest.fixture
def create_customer(api_client):
    def do_create_customer(customer):
        return api_client.post('/store/customers/', customer)
    return do_create_customer

@pytest.fixture
def make_customer():
    user = baker.make(User)
    return Customer.objects.get(user_id=user.id)

@pytest.fixture
def get_customer(make_customer):
    return {
        'user_id': make_customer.user_id,
        'phone': make_customer.phone,
        'birth_date': "2025-12-23",
        'membership': make_customer.membership
    }

@pytest.mark.django_db
class TestCreateCustomer:
    def test_if_user_is_anonymous_returns_401(self, create_customer, get_customer):
        response = create_customer(get_customer)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_customer, auth_client, get_customer):
        auth_client()

        response = create_customer(get_customer)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_customer, auth_client):
        auth_client(is_staff=True)

        response = create_customer({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['user_id'] is not None

    # I don't know what to do. When we create a user, customer auto created
    # def test_if_data_is_valid_returns_201(self, create_customer, auth_client, get_customer):
    #     auth_client(is_staff=True)
    #
    #     response = create_customer(get_customer)
    #
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCustomer:

    def test_get_customers_not_staff_returns_403(self, auth_client, api_client):
        auth_client()
        response = api_client.get(f'/store/customers/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_customers_is_staff_returns_200(self, auth_client, api_client, make_customer):
        auth_client(is_staff=True)
        response = api_client.get(f'/store/customers/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_customer_exists_returns_200(self, api_client, make_customer):
        api_client.force_authenticate(user=make_customer.user)
        response = api_client.get(f'/store/customers/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == make_customer.id

@pytest.mark.django_db
class TestUpdateDeleteCustomer:

    def test_patch_customer_returns_200(self, api_client, make_customer):
        api_client.force_authenticate(user=make_customer.user)

        response = api_client.put(f'/store/customers/me/', {'phone': '123123'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['phone'] == '123123'