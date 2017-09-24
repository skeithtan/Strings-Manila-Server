from django.db.models import Model, BooleanField


# This model will remain in the database when discontinued
class DiscontinueableModel(Model):
    is_active = BooleanField(default=True)

    @classmethod
    def all_active(cls):
        return cls.objects.filter(is_active=True)

    def discontinue(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True
