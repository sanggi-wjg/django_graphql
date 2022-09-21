from decimal import Decimal
from functools import lru_cache

from django.db import models
from django.utils.functional import cached_property


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
