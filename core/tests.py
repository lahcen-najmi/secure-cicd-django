import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_employee_list_status(client):
    response = client.get(reverse('employee_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_employee_page(client):
    response = client.get(reverse('add_employee'))
    assert response.status_code == 200
