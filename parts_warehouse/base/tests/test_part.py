from unittest.mock import ANY

import pytest
from django.urls import reverse

from base.factories import PartFactory, CategoryFactory
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_list_returns_full_object():
    parts = PartFactory.create_batch(2)

    response = APIClient().get(reverse("part-list"))

    assert response.status_code == 200
    assert len(response.json()) == len(parts)
    parts_responses = [
        {
            "id": part.id,
            "serial_number": part.serial_number,
            "name": part.name,
            "description": part.description,
            "category_name": part.category.name,
            "quantity": part.quantity,
            "price": part.price,
            "location": part.location
        }
        for part in parts
    ]
    assert all(
        response_element in parts_responses for response_element in response.json()
    )


@pytest.mark.django_db
def test_detail_returns_full_object():
    part = PartFactory.create()

    response = APIClient().get(reverse("part-detail", args=(part.id,)))

    assert response.status_code == 200

    assert response.json() == {
            "id": part.id,
            "serial_number": part.serial_number,
            "name": part.name,
            "description": part.description,
            "category_name": part.category.name,
            "quantity": part.quantity,
            "price": part.price,
            "location": part.location
    }


@pytest.mark.django_db
def test_create_part():
    category = CategoryFactory.create(parent_name=CategoryFactory.create())
    name = "test_name"
    serial_number = "123"
    description = "test"
    quantity = 2
    price = 12.0
    location = {
        "room": "A123",
        "bookcase": "5",
        "shelf": "4",
        "cuvette": "3",
        "column": "2",
        "row": "1"
    }

    data = {
        "serial_number": serial_number,
        "name": name,
        "description": description,
        "category": category.id,
        "quantity": quantity,
        "price": price,
        "location": location
    }

    response = APIClient().post(reverse("part-list"), data,format="json")

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY,
        "serial_number": serial_number,
        "name": name,
        "description": description,
        "category_name": category.name,
        "quantity": quantity,
        "price": price,
        "location": location
    }


@pytest.mark.django_db
def test_create_part_fails_category_without_parent():
    category = CategoryFactory.create()
    name = "test_name"
    serial_number = "123"
    description = "test"
    quantity = 2
    price = 12.0
    location = {
        "room": "A123",
        "bookcase": "5",
        "shelf": "4",
        "cuvette": "3",
        "column": "2",
        "row": "1"
    }

    data = {
        "serial_number": serial_number,
        "name": name,
        "description": description,
        "category": category.id,
        "quantity": quantity,
        "price": price,
        "location": location
    }

    response = APIClient().post(reverse("part-list"), data,format="json")

    assert response.status_code == 400
    assert response.json() == {"category": ["Part cannot be assigned to a Category without a parent."]}


@pytest.mark.django_db
def test_create_part_fails_no_required_fields():
    data = {}

    response = APIClient().post(reverse("part-list"), data)

    assert response.status_code == 400
    assert response.json() == {
        "category": ["This field is required."],
        "location": ["This field is required."],
        "name": ["This field is required."],
        "price": ["This field is required."],
        "quantity": ["This field is required."],
        "serial_number": ["This field is required."]
    }


@pytest.mark.django_db
def test_update_part():
    category = CategoryFactory.create(parent_name=CategoryFactory.create())
    part = PartFactory.create(category=category)
    new_name = "new_name"
    new_description = "new_description"

    data = {
        "name": new_name,
        "description": new_description,
        "serial_number": part.serial_number,
        "location": part.location,
        "quantity": part.quantity,
        "price": part.price,
        "category": part.category.id
    }

    response = APIClient().put(reverse("part-detail", args=(part.id,)), data, format="json")

    assert response.status_code == 200
    assert response.json() == {
        "id": part.id,
        "serial_number": part.serial_number,
        "name": new_name,
        "description": new_description,
        "category_name": part.category.name,
        "quantity": part.quantity,
        "price": part.price,
        "location": part.location
    }


@pytest.mark.django_db
def test_delete_part():
    part = PartFactory.create()

    response = APIClient().delete(reverse("part-detail", args=(part.id,)))

    assert response.status_code == 204
