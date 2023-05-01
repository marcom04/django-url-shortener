from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task
from celery.utils.log import get_task_logger

from apps.mappings.models import Mapping

logger = get_task_logger(__name__)


@shared_task(time_limit=120)
def cleanup_mappings():
    """
    Look for expired mappings and delete them.
    For mappings related to users, notify the owners via e-mail.
    """
    all_expired = Mapping.objects.select_related('user').expired()
    # get distinct users for the expired mappings
    users = all_expired.values('user_id', 'user__email', 'user__name').distinct()
    for user in users:
        # save user's mapping data into the users dict before deleting the queryset
        user['mappings'] = all_expired.filter(user_id=user['user_id']).values('key', 'target', 'visits')

    count, _ = all_expired.delete()
    logger.info(f"Deleted {count} expired mappings.")

    # send e-mail notifications
    for user in users:
        msg_plain = render_to_string(
            'email/expired_mappings.txt',
            {
                'name': user['user__name'],
                'mappings': user['mappings']
            }
        )
        try:
            send_mail(
                '[urlcut] Expired URLs',
                msg_plain,
                'noreply@urlcut.com',
                [user['user__email']],
                fail_silently=False
            )
        except IOError as e:
            logger.error(f'cleanup_mappings - Error sending e-mail: {e}')

    return count

