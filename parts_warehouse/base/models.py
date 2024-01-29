from djongo import models
from .validators import validate_category_has_parent


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_name = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Part(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        "base.Category",
        on_delete=models.PROTECT,
        related_name="parts",
        validators=[validate_category_has_parent]
    )
    quantity = models.IntegerField()
    price = models.FloatField()
    location = models.JSONField()

    def __str__(self):
        return f'{self.name} ({self.serial_number})'
