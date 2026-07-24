from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from .models import Notification


def send_notification_to_user(user_id, title, body):
    """Persist a notification and push it to the user's WebSocket group, if connected."""
    notification = Notification.objects.create(recipient_id=user_id, title=title, body=body)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'send_notification',
            'id': notification.id,
            'title': title,
            'body': body,
            'timestamp': timezone.now().isoformat(),
        }
    )
    return notification
