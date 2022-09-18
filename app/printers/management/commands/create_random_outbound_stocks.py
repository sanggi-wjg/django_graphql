import random

from django.core.management import BaseCommand

from app.core.colorful import green, cyan, yellow
from app.printers.models import OutboundStock, OutboundInvoice, OutboundEncryptedInvoice


class Command(BaseCommand):
    help = 'Create random articles'

    def add_arguments(self, parser):
        parser.add_argument('create_size', type=int)

    def handle(self, *args, **options):
        create_size = options.get('create_size', 10)

        for _ in range(create_size):
            stock = OutboundStock.objects.create_with_faker()
            green(f"[Create Outbound Stock] Code: {stock.product_code} /t TC: {stock.transfer_company}")

            rand = random.randint(0, 1)
            if rand:
                invoice = OutboundInvoice.objects.create_with_faker(stock)
                cyan(f"[Create Invoice] Code: {invoice.stock.product_code} \t InvoiceNo : {invoice.invoice_no}")

            else:
                encrypted = OutboundEncryptedInvoice.objects.create_with_faker(stock)
                yellow(f"[Create Encrypted] Code: {encrypted.stock.product_code}\t Sign: {encrypted.sign}\t Encrypted: {encrypted.encrypted_data}")
