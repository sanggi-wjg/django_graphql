import graphene

from app.printers.models import OutboundStock


class GetOutboundInvoiceInput(graphene.InputObjectType):
    product_code = graphene.String(required=True)


class GetOutboundInvoiceMutation(graphene.Mutation):
    class Meta:
        description = "출고 주문 송장 정보 가져오기"

    class Arguments:
        input = GetOutboundInvoiceInput(required=True)

    is_success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input: dict):
        try:
            stock = OutboundStock.objects.get(product_code=input['product_code'])
            printer_output = 123

            return cls(is_success=True)

        except (OutboundStock.DoesNotExist,):
            return cls(is_success=False)
