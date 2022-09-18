import random
from base64 import b64encode
from enum import Enum
from secrets import token_bytes

from django.db import models
from faker import Faker


class TransferCompany(Enum):
    EMS = "EMS"
    EMS_PREMIUM = "EMS_PREMIUM"
    EMS_TAIWAN = "EMS_TAIWAN"
    PANTOS = "PANTOS"
    CAINAO = "CAINAO"
    YTO = "YTO"
    YUNDA = "YUNDA"


CHOICE_TRANSFER_COMPANY = (
    (TransferCompany.EMS, 'EMS'),
    (TransferCompany.EMS_PREMIUM, 'EMS_PREMIUM'),
    (TransferCompany.EMS_TAIWAN, 'EMS_TAIWAN'),
    (TransferCompany.PANTOS, 'PANTOS'),
    (TransferCompany.CAINAO, 'CAINAO'),
    (TransferCompany.YTO, 'YTO'),
    (TransferCompany.YUNDA, 'YUNDA'),
)

fake = Faker()
Faker.seed(0)


class OutboundStockManager(models.Manager):

    def create_with_faker(self, transfer_company: TransferCompany = None):
        if transfer_company is None:
            transfer_company = random.choice(list(TransferCompany)).value
        fake_code = f"{fake.ean(length=8)}{random.randint(1000, 9999)}"

        return self.create(
            product_code=fake_code,
            package_code=fake_code,
            transfer_company=transfer_company
        )


class OutboundStock(models.Model):
    objects = OutboundStockManager()

    product_code = models.CharField(max_length=250)
    package_code = models.CharField(max_length=250)
    transfer_company = models.CharField(max_length=50, choices=CHOICE_TRANSFER_COMPANY)

    @property
    def last_invoice(self):
        return self.invoice.last()

    @property
    def last_encrypted_invoice(self):
        return self.encrypted_invoice.last()


class OutboundInvoiceManager(models.Manager):

    def create_with_faker(self, stock: OutboundStock):
        return self.create(
            stock=stock,
            invoice_no=fake.ean(length=13)
        )


class OutboundInvoice(models.Model):
    objects = OutboundInvoiceManager()

    invoice_no = models.CharField(max_length=250)

    stock = models.ForeignKey(
        "OutboundStock", on_delete=models.CASCADE, related_name='invoice'
    )


class OutboundEncryptedInvoiceManager(models.Manager):

    def create_with_faker(self, stock: OutboundStock):
        return self.create(
            stock=stock,
            sign=fake.ein(),
            encrypted_data=b64encode(token_bytes(32)).decode()
        )


class OutboundEncryptedInvoice(models.Model):
    objects = OutboundEncryptedInvoiceManager()

    encrypted_data = models.CharField(max_length=250)
    sign = models.CharField(max_length=250)

    stock = models.ForeignKey(
        "OutboundStock", on_delete=models.CASCADE, related_name='encrypted_invoice'
    )
