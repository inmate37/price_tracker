# Python
from typing import Any
from datetime import datetime

# Django
from django.db.models import (
    DateTimeField,
    Manager,
    Model,
    QuerySet,
    query
)


class FullTrackingQuerySet(QuerySet):

    def not_deleted(self) -> Any:
        return self.filter(dt_deleted__isnull=True)

    def deleted(self) -> Any:
        return self.filter(dt_deleted__isnull=False)

    def delete(self) -> None:
        self.update(dt_deleted=datetime.now())


class FullTrackingManager(Manager):

    def get_queryset(self) -> query.QuerySet['FullTrackingModel']:
        return FullTrackingQuerySet(
            self.model,
            using=self._db
        )

    def not_deleted(self) -> Any:
        return self.get_queryset().not_deleted()

    def deleted(self) -> Any:
        return self.get_queryset().deleted()


class TrackingModel(Model):

    dt_created: DateTimeField = DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class FullTrackingModel(TrackingModel):

    dt_updated: DateTimeField = DateTimeField(
        verbose_name='дата обновления',
        auto_now=True
    )
    dt_deleted: DateTimeField = DateTimeField(
        verbose_name='дата удаления',
        null=True,
        blank=True
    )
    objects = FullTrackingManager()

    def delete(self) -> None:
        self.dt_deleted = datetime.now()
        self.save(update_fields=('dt_deleted',))

    class Meta:
        abstract = True
