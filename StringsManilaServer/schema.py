import entity_management.schema
from graphene import (
    Schema,
    ObjectType
)


class Query(entity_management.schema.Query, ObjectType):
    pass

schema = Schema(query=Query)
