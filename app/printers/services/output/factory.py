from typing import Dict

from app.printers.models import TransferCompany
from app.printers.services.output.printer_output_maker import PrinterOutputMaker, TaiwanAdapter
from app.printers.services.output.provider.encrypted import EncryptedData
from app.printers.services.output.provider.html import HTMLProductCodeLabel, HTMLPackageCodeLabel, HTMLLabelTaiwan
from app.printers.services.output.provider.pdf import PdfUrl


def make_printer_output(transfer_company: TransferCompany):
    factories: Dict[TransferCompany, PrinterOutputMaker] = {
        TransferCompany.EMS: HTMLProductCodeLabel(),
        TransferCompany.EMS_PREMIUM: HTMLPackageCodeLabel(),
        TransferCompany.EMS_TAIWAN: TaiwanAdapter(HTMLLabelTaiwan()),
        TransferCompany.CAINAO: EncryptedData(),
        TransferCompany.PANTOS: PdfUrl(),
    }
    factory = factories.get(transfer_company)

    assert factory, "factory is not set"
    return factory
