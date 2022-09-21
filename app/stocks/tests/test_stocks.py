from decimal import Decimal

from django.test import TestCase

from app.stocks.models import Stock, calc_something


class StockTestCase(TestCase):
    """
    stocks = [
        Stock("Product-1", Decimal(100), Decimal(10)),
        Stock("Product-2", Decimal(200), Decimal(10)),
        Stock("Product-3", Decimal(300), Decimal(10)),
        Stock("Product-4", Decimal(100), Decimal(10)),
        Stock("Product-5", Decimal(400), Decimal(10)),
        Stock("Product-6", Decimal(200), Decimal(10)),
    ]
    """

    def test_0001(self):
        # given
        stocks = [
            Stock.objects.create(product_name="Product-1", price=Decimal(100), discount_price=Decimal(10)),
            Stock.objects.create(product_name="Product-2", price=Decimal(200), discount_price=Decimal(10)),
            Stock.objects.create(product_name="Product-3", price=Decimal(300), discount_price=Decimal(10)),
            Stock.objects.create(product_name="Product-4", price=Decimal(100), discount_price=Decimal(10)),
            Stock.objects.create(product_name="Product-5", price=Decimal(400), discount_price=Decimal(10)),
            Stock.objects.create(product_name="Product-6", price=Decimal(200), discount_price=Decimal(10))
        ]

        # when
        # then
        for stock in stocks:
            print(stock.pay_price, calc_something.cache_info())

        print('\n\n')
        for stock in stocks:
            print(stock.pay_price_2)
            print(stock.pay_price_2)
