import factory
import random
from base.models import Category, Part

example_variable = "test"

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class PartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Part

    serial_number = factory.Faker("name")
    name = factory.Faker("name")
    description = factory.Faker("text")
    category = factory.SubFactory(CategoryFactory)
    quantity = random.randint(1, 100)
    price = float(random.randint(1, 100))
    location = {
        "room": example_variable,
        "bookcase": example_variable,
        "shelf": example_variable,
        "cuvette": example_variable,
        "column": example_variable,
        "row": example_variable
    }
