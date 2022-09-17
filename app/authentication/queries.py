import graphene
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from app.authentication.models import User
from app.authentication.types import UserType
from app.core.graphen_utils import get_id_from_gid


class UserQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')
    # user = relay.Node.Field(UserType)
    # user_all = graphene.List(UserType)

    user = graphene.Field(UserType, user_id=graphene.ID(required=True))
    users = DjangoFilterConnectionField(UserType)

    def resolve_user(self, info: ResolveInfo, user_id: str):
        try:
            return User.objects.get(pk=get_id_from_gid(user_id))
        except User.DoesNotExist:
            return None
