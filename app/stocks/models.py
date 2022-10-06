from decimal import Decimal
from functools import lru_cache

from django.db import models
from django.utils.functional import cached_property


class CategoryNameChoices(models.TextChoices):
    """ 카테고리 종류 """

    COSMETIC = "COSMETIC", "Cosmetic"
    FOOD = "FOOD", "Food"
    BOOK = "BOOK", "Book"


# class WarehouseUsingCategoryChoices(models.IntegerChoices):
#     help = "창고별 "

class Category(models.Model):
    category_name = models.CharField(choices=CategoryNameChoices.choices, max_length=250, null=True)
    something_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_category_name_valid",
                check=models.Q(category_name__in=CategoryNameChoices.values),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_something_price_valid",
                check=models.Q(something_price__gte=0),
            )
        ]

    def __str__(self):
        return f"<Category {self.category_name} {self.something_price}>"


class Stock(models.Model):
    product_name = models.CharField(max_length=250)

    price = models.DecimalField(max_digits=5, decimal_places=0)
    discount_price = models.DecimalField(max_digits=5, decimal_places=0)

    @property
    def pay_price(self):
        return calc_something(self.price, self.discount_price)

    @cached_property
    def pay_price_2(self):
        return self.price - self.discount_price


@lru_cache(typed=True)
def calc_something(a: Decimal, b: Decimal) -> Decimal:
    return a - b
