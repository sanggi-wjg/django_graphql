from typing import Union

from app.printers.models import OutboundStock
from app.printers.services.output.printer_output_maker import PrinterOutputMaker


class PdfUrl(PrinterOutputMaker):
    help = "PDF URL"

    def get_output(self, stock: OutboundStock) -> Union[str, dict]:
        assert stock.last_invoice, "need outbound_invoice"

        return f"{self.pdf_url}{stock.last_invoice.invoice_no}"
