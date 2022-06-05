import typing as t
from enum import Enum
from service.mailer.base import MailerService
import requests
import logging

logging.getLogger().setLevel(logging.INFO)

class UnioneTemplate(str, Enum):
    SEND_PASSWORD_CODE = "528888ae-aece-11ec-9797-2a440d9a0bd2"
    SEND_PASSWORD_CHANGE = "3b78b4c2-aece-11ec-98b1-ca5b43537ee6"
    SEND_PLAN_CHANGE = "65c7171e-aece-11ec-9e40-6a94fda5f5e4"
    SEND_SUBS_CANCEL = "78c9e080-aece-11ec-8fe0-42680be9d0a9"
    SEND_GREETINGS_YEAR = "c4869a96-aecd-11ec-9d6b-2a440d9a0bd2"
    SEND_GREETINGS = "4d8757be-aecd-11ec-ad0a-2a440d9a0bd2"
    SEND_5DAYS_ALERT = "681047ac-aec9-11ec-9f2c-9ea60a037e47"
    SEND_15DAYS_ALERT = "6f5fb804-9f87-11ec-af0f-e61cfa0e366a"
    SEND_EMAIL_CONFIRM_LINK = "851e5946-af65-11ec-9e5e-72a096553c30"
    SEND_NONACTIVE_TARIFF_ALERT = "0079c9e2-aece-11ec-a3e5-6a94fda5f5e4"
    SEND_NONACTIVE_TARIFF_LAST_ALERT = "25808992-aece-11ec-b3dc-72a096553c30"


class UnioneMailerService(MailerService):
    _api_uri: str
    _api_key: str
    _email_from: str
    _app_host: str

    def __init__(
            self,
            api_uri: str,
            api_key: str,
            email_from: str,
            app_host: str,
    ) -> None:
        self._api_uri = api_uri
        self._api_key = api_key
        self._email_from = email_from
        self._app_host = app_host

    def send_email(
            self,
            email: str,
            text: t.Optional[str] = None,
            template: t.Optional[str] = None,
            subject: t.Optional[str] = None,
            variables: t.Optional[dict[str, t.Union[str, int]]] = None,
    ) -> None:
        response = requests.post(
            self._api_uri + "/email/send.json",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-API-KEY": self._api_key,
            },
            json={
                "message": {
                    "from_email": self._email_from,
                    **({"subject": subject} if subject else {}),
                    "recipients": [
                        {
                            "email": email,
                            **({"substitutions": variables} if variables else {}),
                        }
                    ],
                    **({"body": {"plaintext": text}} if text else {}),
                    **({"template_id": template} if template else {}),
                    "global_language": "ru",
                    "template_engine": "simple",
                }
            },
        )
        if response.status_code != requests.codes.ok:
            logging.error(
                response.text
            )
        else:
            logging.info("message sent")

    def send_notification_event(self, email: str, text: str, subject: str) -> None:
        self.send_email(
            email=email,
            text=text,
            subject=subject
        )

    def send_password_code(self, email: str, code: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_PASSWORD_CODE.value,
            variables={"code": str(code)},
        )

    def send_password_change(self, email: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_PASSWORD_CHANGE.value,
        )

    def send_plan_change(self, email: str, tariff_name: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_PLAN_CHANGE.value,
            variables={"new_tariff_name": tariff_name},
        )

    def send_subs_cancel(self, email: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_SUBS_CANCEL.value,
        )

    def send_first_payment_greeting(
        self, email: str, tariff_period_days: int = 30
    ) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_GREETINGS_YEAR.value
            if tariff_period_days == 360
            else UnioneTemplate.SEND_GREETINGS.value,
        )

    def send_monthly_tariff_notification(self, email: str, date: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_5DAYS_ALERT.value,
            variables={"date": date},
        )

    def send_yearly_tariff_notification(self, email: str, date: str) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_15DAYS_ALERT.value,
            variables={"date": date},
        )

    def send_email_confirm_link(self, email: str, code: str) -> None:
        app_host = (
            self._app_host
            if self._app_host.startswith("https")
            else f"https://{self._app_host}"
        )

        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_EMAIL_CONFIRM_LINK.value,
            variables={"link": f"{app_host}/verify-email?email={email}&code={code}"},
        )

    def send_email_nonactive_tariff_alert(
        self, email: str, user_name: str, tariff_name: str, take_down_date: str
    ) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_NONACTIVE_TARIFF_ALERT.value,
            variables={
                "name": user_name,
                "take_down_date": take_down_date,
            },
        )

    def send_email_nonactive_tariff_last_alert(
        self, email: str, user_name: str, tariff_name: str, take_down_date: str
    ) -> None:
        self.send_email(
            email=email,
            template=UnioneTemplate.SEND_NONACTIVE_TARIFF_LAST_ALERT.value,
            variables={
                "name": user_name,
                "tariff": tariff_name,
                "take_down_date": take_down_date,
            },
        )
