from typing import Union

from app.printers.models import OutboundStock
from app.printers.services.output.printer_output_maker import PrinterOutputMaker


class EncryptedData(PrinterOutputMaker):
    help = "암호화 데이터"

    def get_output(self, stock: OutboundStock) -> Union[str, dict]:
        assert stock.last_encrypted_invoice, "outbound_encrypted_invoice 필요"

        return {
            "encrypted": stock.last_encrypted_invoice.encrypted_data,
            "sign": stock.last_encrypted_invoice.sign
        }
