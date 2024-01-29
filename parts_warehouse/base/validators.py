from django.core.exceptions import ValidationError


def validate_category_has_parent(value):
    """ Validate that a Part cannot be assigned to a Category without a parent_name (base category). """

    if value and not value.parent_name:
        raise ValidationError("Part cannot be assigned to a Category without a parent.")
