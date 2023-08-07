from django.dispatch import receiver

from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL, operation_event_log
from edx_operation.apps.grade.models import CourseGrade, ExamStatus, Submission, SubsectionGrade


@receiver(OPERATION_EVENT_SIGNAL)
def log_operation_event(event, **kwargs):
    if event.event_type == "operation_event.signals.coursegrade":
        m = event.message
        CourseGrade.objects.update_or_create(
            student_id=m.get("user_id"),
            course_id=m.get("course_id"),
            defaults={
                "percent_grade": m.get("percent_grade"),
                "letter_grade": m.get("letter_grade"),
                "passed": m.get("passed"),
                "grade_summary": m.get("grade_summary"),
            },
        )

    elif event.event_type == "operation_event.signals.subsectiongrade":
        m = event.message
        defaults = {
            "earned_all": m.get("earned_all"),
            "possible_all": m.get("possible_all"),
            "earned_graded": m.get("earned_graded"),
            "possible_graded": m.get("possible_graded"),
        }

        due = m.get("due")
        if due:
            defaults["due"] = due

        SubsectionGrade.objects.update_or_create(
            student_id=m.get("user_id"),
            course_id=m.get("course_id"),
            usage_key=m.get("usage_key"),
            defaults=defaults,
        )

    elif event.event_type == "operation_event.signals.blockcompletion":
        m = event.message
        defaults = {
            "complete": m.get("subsection_complete"),
            "completion_block": m.get("block_key"),
            "client_ip": event.client_ip,
        }

        due = m.get("due")
        if due:
            defaults["due"] = due

        SubsectionGrade.objects.update_or_create(
            student_id=m.get("user_id"),
            course_id=m.get("context_key"),
            usage_key=m.get("subsection_usage_key"),
            defaults=defaults,
        )

    elif event.event_type == "operation_event.signals.proctoredexamstudentattempt":
        m = event.message
        exam = m.get("proctored_exam")

        ExamStatus.objects.update_or_create(
            student_id=m.get("user_id"),
            course_id=exam.get("course_id"),
            usage_key=exam.get("content_id"),
            defaults={
                "is_active": exam.get("is_active"),
                "status": m.get("status"),
                "deleted": event.deleted,
            },
        )

    elif event.event_type == "operation_event.signals.submission":
        m = event.message
        student_item = m.get("student_item")

        Submission.objects.update_or_create(
            uuid=m.get("uuid"),
            defaults={
                "student_id": m.get("user_id"),
                "course_id": student_item.get("course_id"),
                "usage_key": student_item.get("item_id"),
                "submitted_at": m.get("submitted_at"),
                "status": m.get("status"),
            },
        )

    elif event.event_type == "operation_event.signals.score":
        m = event.message
        uuid = m.get("submission").get("uuid")
        if not uuid:
            return

        points_possible = m.get("points_possible")
        score = (m.get("points_earned") / points_possible) if points_possible else 0

        Submission.objects.update_or_create(
            uuid=uuid,
            defaults={
                "score": score,
                "scored_at": m.get("created_at"),
                "score_reset": m.get("reset"),
            },
        )
