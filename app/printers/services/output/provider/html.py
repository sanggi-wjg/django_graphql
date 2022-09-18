from typing import Union

from app.printers.models import OutboundStock
from app.printers.services.output.printer_output_maker import PrinterOutputMaker, PrinterOutputMakerTaiwan


class HTMLLabel(PrinterOutputMaker):
    help = "HTML Label"

    def label_content(self, stock: OutboundStock) -> str:
        raise NotImplementedError("[label_content] not implemented")

    def get_output(self, stock: OutboundStock) -> Union[str, dict]:
        assert stock.last_invoice, "need outbound_invoice"

        return f"""
        <html>
        <body>
        <img src="{self.invoice_barcode_url}{stock.last_invoice.invoice_no}">
        {self.label_content(stock)}
        <body>
        <html>
        """


class HTMLProductCodeLabel(HTMLLabel):

    def label_content(self, stock: OutboundStock) -> str:
        return f"<h3>ProductCode {stock.product_code}</h3>"


class HTMLPackageCodeLabel(HTMLLabel):

    def label_content(self, stock: OutboundStock) -> str:
        return f"<h3>PackageCode {stock.package_code}</h3>"


class HTMLLabelTaiwan(PrinterOutputMakerTaiwan):
    invoice_barcode_url = "https://some.file.com/barcode/invoice/taiwan/"

    def diff_get_output(self, stock: OutboundStock) -> Union[str, dict]:
        assert stock.last_invoice, "need outbound_invoice"

        if not self.is_valid_customer_pin_number(stock.last_invoice.invoice_no):
            raise Exception("앗...")

        return f"""
                <html>
                <body>
                <img src="{self.invoice_barcode_url}{stock.last_invoice.invoice_no}">
                <body>
                <html>
                """
