from django_extensions.db.fields import AutoSlugField
from django.db.models import CASCADE, CharField, ForeignKey, Model


class State(Model):
    name = CharField(max_length=50, unique=True, null=False, blank=False)
    name_slug = AutoSlugField(populate_from=('name', ), unique=True, db_index=True)


class City(Model):
    name = CharField(max_length=50, unique=True, null=False, blank=False)
    name_slug = AutoSlugField(populate_from=('name', ), unique=True, db_index=True)

    state = ForeignKey(to=State, on_delete=CASCADE, related_name='cities', null=False)

    class Meta:
        unique_together = ('name', 'state')
