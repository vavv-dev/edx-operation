import traceback
from django.db.models import BooleanField, CharField, DateTimeField, SmallIntegerField, TextField

from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.core.utils.common import admin_action


class OperationEvent(TimeStampedModel):
    class Meta:
        verbose_name = "이벤트"
        verbose_name_plural = verbose_name

    event_type = CharField(max_length=255, db_index=True)
    event_time = DateTimeField()
    source_data = TextField()
    success = BooleanField(null=True, blank=True)
    error = TextField(null=True, blank=True)
    retry_count = SmallIntegerField(default=0)

    @admin_action
    def retry(self):
        from .service import OPERATION_EVENT_SIGNAL, OperationEvent as Event

        self.retry_count += 1

        try:
            event = Event.from_data(self.source_data)
            OPERATION_EVENT_SIGNAL.send_event(event=event)
        except Exception as e:
            self.error = traceback.format_exc()
            self.success = False
        else:
            self.success = True
        finally:
            self.save()
