from django.db import models
from django_extensions.db.models import TimeStampedModel


class OperationEventError(TimeStampedModel):
    event_type = models.CharField(max_length=255, db_index=True)
    event_time = models.DateTimeField()
    error = models.TextField()
    source_data = models.TextField()
    retry_count = models.SmallIntegerField(default=0)
    retry_success = models.BooleanField(null=True, blank=True)
