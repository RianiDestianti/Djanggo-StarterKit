from django.db import models
from models.base_model import BaseModel


class VerificationModel(BaseModel):
    email       = models.CharField(max_length=255, db_index=True)
    value       = models.CharField(max_length=20)

    class Meta:
        db_table    = "verifications"
        managed     = False
