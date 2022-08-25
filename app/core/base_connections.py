import graphene


class PaginationConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    @classmethod
    def resolve_total_count(cls, root, info, **kwargs):
        return root.length

    @classmethod
    def resolve_edge_count(cls, root, info, **kwargs):
        return len(root.edges)
