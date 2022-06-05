import json
import os
import logging

from service.lockbox import LockBox
from service.mailer.unione import UnioneMailerService
from service.aws import send_message_to_dlq
from enum import Enum

logging.getLogger().setLevel(logging.INFO)

# Lockbox init
lockbox = LockBox()
logging.info("Lockbox successfully initialized.")

secret_id = os.environ['LOCKBOX_UNIONE_KEY_ID']
mailgun_credentials = lockbox[secret_id]

# Mailgun init
unione = UnioneMailerService(
    api_uri=os.environ.get("UNIONE_API_URI"),
    api_key=mailgun_credentials["unione_key"],
    email_from=os.environ.get("MAILGUN_EMAIL_FROM"),
    app_host=os.environ.get("APP_HOST"),
)
logging.info("Mailgun successfully initialized.")


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


def handler(event, context):
    messages = event['messages']
    logging.info(f'messages {len(messages)}')
    for msq in messages:
        try:
            data = json.loads(msq['details']['message']['body'])
            logging.info(json.dumps(data))
            template = data['template']
            if template == MessageType.SEND_NOTIFICATION_EVENT:
                unione.send_notification_event(
                    email=data["to"],
                    text=data["text"],
                    subject=data["subject"],
                )
            elif template == MessageType.SEND_PASSWORD_CHANGE:
                unione.send_password_change(
                    email=data["to"],
                )
            elif template == MessageType.SEND_PASSWORD_CODE:
                unione.send_password_code(
                    email=data["to"],
                    code=data['variable'],
                )
            elif template == MessageType.SEND_PLAN_CHANGE:
                unione.send_plan_change(
                    email=data["to"],
                    tariff_name=data['variable'],
                )
            elif template == MessageType.SEND_SUBS_CANCEL:
                unione.send_subs_cancel(
                    email=data["to"],
                )
            elif template == MessageType.SEND_GREETINGS:
                unione.send_first_payment_greeting(
                    email=data["to"],
                    tariff_period_days=data['variable'],
                )
            elif template == MessageType.SEND_5DAYS_ALERT:
                unione.send_monthly_tariff_notification(
                    email=data["to"],
                    date=data['variable'],
                )
            elif template == MessageType.SEND_15DAYS_ALERT:
                unione.send_yearly_tariff_notification(
                    email=data["to"],
                    date=data['variable'],
                )
            elif template == MessageType.SEND_EMAIL_CONFIRM_LINK:
                unione.send_email_confirm_link(
                    email=data["to"],
                    code=data['variable'],
                )
            elif template == MessageType.SEND_NONACTIVE_TARIFF_ALERT:
                unione.send_email_nonactive_tariff_alert(
                    email=data["to"],
                    take_down_date=data['variable'],
                )
            elif template == MessageType.SEND_NONACTIVE_TARIFF_LAST_ALERT:
                unione.send_email_nonactive_tariff_last_alert(
                    email=data["to"],
                    take_down_date=data['variable'],
                )

            logging.info("message sent")


        except Exception:
            send_message_to_dlq(
                body=json.dumps(data)
            )

    return {
        'statusCode': 200,
        'body': 'success',
    }
