import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from app.authentication.types import UserType


class UserQuery(graphene.ObjectType):
    user_all = graphene.List(UserType)

    user = relay.Node.Field(UserType)
    users = DjangoFilterConnectionField(UserType)
