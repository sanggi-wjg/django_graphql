from abc import ABC, abstractmethod
from typing import Union

from app.printers.models import OutboundStock


class PrinterOutputMaker(ABC):
    invoice_barcode_url = "https://some.file.com/barcode/invoice/"
    pdf_url = "https://some.file.com/pdf/"

    @abstractmethod
    def get_output(self, stock: OutboundStock) -> Union[str, dict]:
        raise NotImplementedError("안해도 되는데 명시적으로 가독성 목적으로 사용 함")


class PrinterOutputMakerTaiwan(ABC):

    def is_valid_customer_pin_number(self, invoice_no) -> bool:
        print("대만 쪽은 송장번호와 고유식별번호를 확인해야 한다.")
        return True

    @abstractmethod
    def diff_get_output(self, stock: OutboundStock) -> Union[str, dict]:
        # 뭔가 다르다고 가정...
        pass


class TaiwanAdapter(PrinterOutputMaker):

    def __init__(self, output_maker: PrinterOutputMakerTaiwan):
        self.kls = output_maker

    def get_output(self, stock: OutboundStock) -> Union[str, dict]:
        return self.kls.diff_get_output(stock)
