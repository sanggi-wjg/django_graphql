from django.test import TestCase

from app.printers.models import OutboundStock, TransferCompany, OutboundInvoice, OutboundEncryptedInvoice
from app.printers.services.output.factory import make_printer_output


class PrinterTestCase(TestCase):

    def setUp(self) -> None:
        pass

    def test_ems(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.EMS)
        OutboundInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)
        output = maker.get_output(stock)

        # then
        print(output)
        self.assert_(output)

    def test_ems_premium(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.EMS_PREMIUM)
        OutboundInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)
        output = maker.get_output(stock)

        # then
        print(output)
        self.assert_(output)

    def test_ems_taiwan(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.EMS_TAIWAN)
        OutboundInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)
        output = maker.get_output(stock)

        # then
        print(output)
        self.assert_(output)

    def test_icb(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.CAINAO)
        OutboundEncryptedInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)
        output = maker.get_output(stock)

        # then
        print(output)
        self.assert_(output)

    def test_pantos(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.PANTOS)
        OutboundInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)
        output = maker.get_output(stock)

        # then
        print(output)
        self.assert_(output)

    def test_ems_fail_case(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.EMS)
        OutboundEncryptedInvoice.objects.create_with_faker(stock)

        # when
        maker = make_printer_output(stock.transfer_company)

        # then
        with self.assertRaises(AssertionError):
            _ = maker.get_output(stock)

    def test_fail_case_factory_was_not_declared(self):
        # given
        stock = OutboundStock.objects.create_with_faker(TransferCompany.YUNDA)
        OutboundInvoice.objects.create_with_faker(stock)

        # when
        with self.assertRaises(AssertionError):
            maker = make_printer_output(stock.transfer_company)
            output = maker.get_output(stock)
