import typing as t
import logging
import asyncio

from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import Integer, ForeignKey, DateTime, String
from notifications.stubs.default_categories import NotificationCategory
from enum import Enum

from configuration.database import db
from identities.identity import Identity

from servise.aws import send_message_to_sqs

logging.getLogger().setLevel(logging.INFO)

class MessageType(str, Enum):
    SEND_NOTIFICATION_EVENT = "send_notification_event"
    SEND_PASSWORD_CODE = "send_password_code"
    SEND_PASSWORD_CHANGE = "send_password_change"
    SEND_PLAN_CHANGE = "send_plan_change"
    SEND_SUBS_CANCEL = "send_subs_cancel"
    SEND_GREETINGS = "send_first_payment_greeting"
    SEND_5DAYS_ALERT = "send_monthly_tariff_notification"
    SEND_15DAYS_ALERT = "send_yearly_tariff_notification"
    SEND_EMAIL_CONFIRM_LINK = "send_email_confirm_link"
    SEND_NONACTIVE_TARIFF_ALERT = "send_email_nonactive_tariff_alert"
    SEND_NONACTIVE_TARIFF_LAST_ALERT = "send_email_nonactive_tariff_last_alert"



class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(UUID, primary_key=True, default=uuid4)

    target_user_id = db.Column(Integer, ForeignKey('user_identity.id'))
    category = db.Column(
        db.Enum(NotificationCategory, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=NotificationCategory.CLUB_NEWS.value,
        server_default=NotificationCategory.CLUB_NEWS.value
    )
    payload = db.Column(JSONB, server_default="{}")
    created_at = db.Column(DateTime, default=datetime.utcnow)
    read_at = db.Column(DateTime, nullable=True)

    @classmethod
    async def get_notifications(
            cls,
            target_user: str,
            unread: t.Optional[bool] = None,
            offset: int = 0,
            limit: int = 40,
    ):

        notifications_query = Notification.query.where(Notification.target_user_id == target_user)
        if unread is not None:
            notifications_query = notifications_query.where(Notification.read_at == None)

        notifications = await notifications_query.gino.all()

        result = []
        for k in notifications[offset: offset + limit]:
            result.append(k.__values__)

        return result

    @classmethod
    async def make_notification_read(
            cls,
            notification_ids: t.List[str]
    ) -> int:

        updated_notifications = await Notification.query.where(Notification.id.in_(notification_ids)).gino.all()

        result = 0
        for notif in updated_notifications:
            login = await notif.update(read_at=datetime.now()).apply()
            logging.info(str(login))
            result += 1

        return result

    @classmethod
    async def create_notification(
            cls,
            target_user_id: str,
            category: NotificationCategory,
            payload: JSONB
    ) -> str:

        notification_corrutine = Notification.create(
            target_user_id=target_user_id,
            category=category,
            payload=payload,
        )

        identity_corrutine = Identity.find_by_id_or_slug(
            user_id=target_user_id
        )

        [notification, identity] = await asyncio.gather(notification_corrutine, identity_corrutine)

        await send_message_to_sqs(
            email=identity.email,
            subject="Уведомление создано",
            text="УСПЕХ",
            template=MessageType.SEND_NOTIFICATION_EVENT.value
        )

        return str(notification.id) + ' | ' + str(identity.email) + ' | ' + str(category)

    @classmethod
    async def send_password_code(
            cls,
            email: str,
            code: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=code,
            template=MessageType.SEND_PASSWORD_CODE.value
        )

        return '200'

    @classmethod
    async def send_password_change(
            cls,
            email: str,
            code: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            template=MessageType.SEND_PASSWORD_CHANGE.value
        )

        return '200'

    @classmethod
    async def send_plan_change(
            cls,
            email: str,
            tariff_name: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=tariff_name,
            template=MessageType.SEND_PLAN_CHANGE.value
        )

        return '200'

    @classmethod
    async def send_subs_cancel(
            cls,
            email: str,
    ) -> str:

        await send_message_to_sqs(
            email=email,
            template=MessageType.SEND_SUBS_CANCEL.value
        )

        return '200'

    @classmethod
    async def send_first_payment_greeting(
            cls,
            email: str,
            days: int
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=days,
            template=MessageType.SEND_GREETINGS.value
        )

        return '200'

    @classmethod
    async def send_monthly_tariff_notification(
            cls,
            email: str,
            date: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=date,
            template=MessageType.SEND_5DAYS_ALERT.value
        )

        return '200'

    @classmethod
    async def send_yearly_tariff_notification(
            cls,
            email: str,
            date: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=date,
            template=MessageType.SEND_15DAYS_ALERT.value
        )

        return '200'

    @classmethod
    async def send_email_confirm_link(
            cls,
            email: str,
            code: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=code,
            template=MessageType.SEND_EMAIL_CONFIRM_LINK.value
        )

        return '200'

    @classmethod
    async def send_email_nonactive_tariff_alert(
            cls,
            email: str,
            date: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=date,
            template=MessageType.SEND_NONACTIVE_TARIFF_ALERT.value
        )

        return '200'

    @classmethod
    async def send_email_nonactive_tariff_last_alert(
            cls,
            email: str,
            date: str
    ) -> str:

        await send_message_to_sqs(
            email=email,
            variable=date,
            template=MessageType.SEND_NONACTIVE_TARIFF_LAST_ALERT.value
        )

        return '200'
