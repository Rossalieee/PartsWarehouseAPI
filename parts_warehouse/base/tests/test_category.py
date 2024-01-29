from unittest.mock import ANY

import pytest
from django.db.models import ProtectedError
from django.urls import reverse

from base.factories import CategoryFactory, PartFactory
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_list_returns_full_object():
    parent_category = CategoryFactory.create()
    child_category = CategoryFactory.create(parent_name=parent_category)

    response = APIClient().get(reverse("category-list"))

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "id": parent_category.id,
            "name": parent_category.name,
            "parent_name": None,
            "children": [child_category.id]
        },
        {
            "id": child_category.id,
            "name": child_category.name,
            "parent_name": parent_category.id,
            "children": []
        }
    ]


@pytest.mark.django_db
def test_detail_returns_full_object():
    category = CategoryFactory.create()

    response = APIClient().get(reverse("category-detail", args=(category.id,)))

    assert response.status_code == 200

    assert response.json() == {
            "id": category.id,
            "name": category.name,
            "parent_name": category.parent_name,
            "children": []
        }


@pytest.mark.django_db
def test_create_category():
    parent = CategoryFactory.create()
    category_name = "test_category"

    data = {"name": category_name, "parent_name": parent.id}

    response = APIClient().post(reverse("category-list"), data)

    assert response.status_code == 201
    assert response.json() == {
        "id": ANY,
        "name": category_name,
        "parent_name": parent.id,
        "children": []
    }


@pytest.mark.django_db
def test_create_category_fails_no_name():
    parent = CategoryFactory.create()

    data = {"parent_name": parent.id}

    response = APIClient().post(reverse("category-list"), data)

    assert response.status_code == 400
    assert response.json() == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_update_category():
    category = CategoryFactory.create()
    new_name = "new_name"

    data = {"name": new_name}

    response = APIClient().put(reverse("category-detail", args=(category.id,)), data)

    assert response.status_code == 200
    assert response.json() == {
        "id": ANY,
        "name": new_name,
        "parent_name": None,
        "children": []
    }


@pytest.mark.django_db
def test_delete_category():
    category = CategoryFactory.create()

    response = APIClient().delete(reverse("category-detail", args=(category.id,)))

    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_category_not_allowed_when_parts_assigned():
    category = CategoryFactory.create()
    PartFactory.create(category=category)

    with pytest.raises(ProtectedError):
        APIClient().delete(reverse("category-detail", args=(category.id,)))


@pytest.mark.django_db
def test_delete_category_not_allowed_when_parts_assigned_to_child():
    category = CategoryFactory.create()
    child_category = CategoryFactory.create(parent_name=category)
    PartFactory.create(category=child_category)

    with pytest.raises(ProtectedError):
        APIClient().delete(reverse("category-detail", args=(category.id,)))
