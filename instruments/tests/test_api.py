import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals
from datetime import date

@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(username='testuser', password='password')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_get_inventory(auth_client):
    Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                             item="Housle", description="Stradivarius")
    response = auth_client.get("/instruments/api/inventory/")
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_post_inventory(auth_client):
    data = {
        "group": "smyčce",
        "subgroup": "housle",
        "subsubgroup": "nástroj",
        "item": "Housle",
        "description": "Stradivarius"
    }
    response = auth_client.post("/instruments/api/inventory/", data, format="json")
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_purchases(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    Purchases.objects.create(inventory_item=inv, purchase_date=date.today(),
                             supplier="Dodavatel", amount=1000, currency="CZK", invoice="1234")
    response = auth_client.get("/instruments/api/purchases/")
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_post_purchases(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    data = {
        "inventory_item": inv.id,
        "purchase_date": str(date.today()),
        "supplier": "Dodavatel",
        "amount": 1000,
        "currency": "CZK",
        "invoice": "1234",
        "notes": "Poznámka"
    }
    response = auth_client.post("/instruments/api/purchases/", data, format="json")
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_rentals(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    Rentals.objects.create(inventory_item=inv, renter_name="Jan", rental_date=date.today(),
                           rental_type="short-term")
    response = auth_client.get("/instruments/api/rentals/")
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_post_rentals(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    data = {
        "inventory_item": inv.id,
        "renter_name": "Test User",
        "rental_date": "2025-09-14",
        "return_date": "2025-09-20",
        "rental_type": "long-term"
    }
    response = auth_client.post("/instruments/api/rentals/", data, format="json")
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_servicing(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    Servicing.objects.create(inventory_item=inv, service_date=date.today(), supplier="Servis",
                             amount=100, currency="CZK", invoice="1234")
    response = auth_client.get("/instruments/api/servicing/")
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_post_servicing(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    data = {
        "inventory_item": inv.id,
        "service_date": str(date.today()),
        "supplier": "Servis",
        "amount": 100,
        "currency": "CZK",
        "invoice": "1234",
        "notes": "Poznámka"
    }
    response = auth_client.post("/instruments/api/servicing/", data, format="json")
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_disposals(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    Disposals.objects.create(inventory_item=inv, disposal_date=date.today(), disposal_reason="vyřazení")
    response = auth_client.get("/instruments/api/disposals/")
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_post_disposals(auth_client):
    inv = Inventory.objects.create(group="smyčce", subgroup="housle", subsubgroup="nástroj",
                                   item="Housle", description="Stradivarius")
    data = {
        "inventory_item": inv.id,
        "disposal_date": str(date.today()),
        "disposal_reason": "vyřazení",
        "notes": "Poznámka"
    }
    response = auth_client.post("/instruments/api/disposals/", data, format="json")
    assert response.status_code == 201