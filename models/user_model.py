from django.db import models
from models.base_model import SoftDelete
from models.role_model import RoleModel


class UserModel(SoftDelete):
    __hidden__  = ['password']

    role        = models.ForeignKey(RoleModel, on_delete=models.DO_NOTHING, db_column='role_id', related_name='users')
    name        = models.CharField(max_length=255)
    email       = models.CharField(max_length=255, unique=True)
    phone       = models.CharField(max_length=30, null=True, blank=True)
    password    = models.CharField(max_length=255)
    avatar      = models.CharField(max_length=500, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table    = "users"
        managed     = False
