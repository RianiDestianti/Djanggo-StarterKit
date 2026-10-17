from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    __hidden__  = []

    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    updated_at  = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return {
            field.attname : getattr(self, field.attname)
            for field in self._meta.concrete_fields
            if field.name not in self.__hidden__
        }

    def destroy(self):
        self.delete()


class SoftDelete(BaseModel):
    deleted_at  = models.DateTimeField(null=True, blank=True)

    objects       = SoftDeleteManager()
    with_trashed  = models.Manager()

    class Meta:
        abstract = True

    def destroy(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
