from datetime import datetime
import json
import logging
import traceback

import attr
from django.conf import settings
from django.dispatch import receiver
from edx_event_bus_kafka.internal.consumer import KafkaEventConsumer
from openedx_events.event_bus import OpenEdxPublicSignal

from edx_operation.apps.event_bus.models import OperationEvent as OperationEventModel


log = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class OperationEvent:
    timestamp: int
    event_type: str
    message: dict
    created: bool
    deleted: bool
    time: datetime
    request_username: str
    client_ip: str
    user_agent: str
    source: str
    container_id: str
    container_name: str

    @classmethod
    def from_data(cls, data):
        event = cls(**json.loads(data))
        setattr(event, "_source_data", data)
        return event

    @property
    def source_data(self):
        return getattr(self, "_source_data", None)


OPERATION_EVENT_SIGNAL = OpenEdxPublicSignal(
    event_type=getattr(settings, "EVENT_BUS_TOPIC_NAME", "operation_event.signals"),
    data={"event": OperationEvent},
)


class OperationEventConsumer(KafkaEventConsumer):
    def determine_signal(self, msg):
        if self.topic == OPERATION_EVENT_SIGNAL.event_type:
            return OPERATION_EVENT_SIGNAL

        return super().determine_signal(msg)

    def emit_signals_from_message(self, msg, signal):
        if self.topic == OPERATION_EVENT_SIGNAL.event_type:
            success = True
            error = None
            try:
                signal.send_event_with_custom_metadata({}, **msg.value())
            except Exception as e:
                log.error(e, exc_info=True)
                success = False
                error = traceback.format_exc()
            finally:
                event = msg.value().get("event")
                OperationEventModel.objects.create(
                    event_type=event.event_type,
                    event_time=event.time,
                    source_data=event.source_data.decode("utf-8"),
                    success=success,
                    error=error,
                )
                return

        super().emit_signals_from_message(msg, signal)

    def _deserialize_message_value(self, msg, signal):
        if self.topic == OPERATION_EVENT_SIGNAL.event_type:
            return {"event": OperationEvent.from_data(msg.value())}

        return super()._deserialize_message_value(msg, signal)


@receiver(OPERATION_EVENT_SIGNAL)
def operation_event_log(event, **kwargs):
    if settings.DEBUG:
        print(json.dumps(attr.asdict(event), indent=4, ensure_ascii=False))
