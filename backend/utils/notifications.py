# utils/notifications.py
from backend.models.model_notifications import Notification

def create_notification(
    db,
    sender_id: int,
    recipient_id: int,
    notif_type: str,
    message: str,
    post_id: int = None,
    comment_id: int = None,
):
    """
    Generic reusable notification creator.
    Use this helper in any router to create notifications.
    """
    # Don't notify yourself
    if sender_id == recipient_id:
        return

    notif = Notification(
        sender_id=sender_id,
        recipient_id=recipient_id,
        type=notif_type,
        post_id=post_id,
        comment_id=comment_id,
        message=message,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif
