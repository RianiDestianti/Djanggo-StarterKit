from django.db import models
from models.base_model import SoftDelete


class RoleModel(SoftDelete):
    name        = models.CharField(max_length=50)

    class Meta:
        db_table    = "roles"
        managed     = False
