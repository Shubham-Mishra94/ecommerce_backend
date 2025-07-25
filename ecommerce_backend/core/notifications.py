from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_order_status(order):
    channel_layer = get_channel_layer()
    group_name = f"user_{order.user.id}_orders"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'order_status_update',
            'order_id': order.id,
            'new_status': order.status,
        }
    )

    