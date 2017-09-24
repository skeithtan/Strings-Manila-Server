from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    PositiveIntegerField
)

from StringsManilaServer.models import DiscontinueableModel


class MaterialType(DiscontinueableModel):
    name = CharField(max_length=64)


class Size(DiscontinueableModel):
    name = CharField(max_length=64)


class Color(DiscontinueableModel):
    name = CharField(max_length=64)
    hex = CharField(max_length=6)

    def __str__(self):
        return f"{self.name} - #{self.hex}"


class Material(DiscontinueableModel):
    material_type = ForeignKey(MaterialType)
    tier = ForeignKey(Size, null=True, on_delete=CASCADE)
    color = ForeignKey(Color, null=True, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)
