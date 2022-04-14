from course_app.models import Course
from payments_app.choices import PaymentStatusChoices
from payments_app.models import Card, PaymentCourse
from rest_framework.validators import ValidationError


def validate_buy_course_data(user, course_id, pm_id):
    if not Course.objects.filter(id=course_id).exists():
        raise ValidationError({'course_id': 'Unknown course ID'})

    queryset = PaymentCourse.objects.filter(
        course_id=course_id,
        user=user,
        payment__status=PaymentStatusChoices.SUCCEEDED
    )
    if queryset.exists():
        raise ValidationError({'course_id': 'You have already purchased this course!'})

    process_statuses = [
            PaymentStatusChoices.REQUIRES_CONFIRMATION,
            PaymentStatusChoices.REQUIRES_ACTION,
            PaymentStatusChoices.PROCESSING,
            PaymentStatusChoices.REQUIRES_CAPTURE,
        ]
    queryset = PaymentCourse.objects.filter(
        course_id=course_id,
        user=user,
        payment__status__in=process_statuses
    )
    if queryset.exists():
        raise ValidationError({
            'course_id': 'You cannot purchase this course until previous operation is completed'
        })

    if not Card.objects.filter(pm_id=pm_id).exists():
        raise ValidationError({'pm_id': 'Unknown payment method ID'})

    return course_id, pm_id