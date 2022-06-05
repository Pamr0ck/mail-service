import typing as t


class MailerService(t.Protocol):
    _api_uri: str
    _api_key: str
    _email_from: str
    _app_host: str

    def send_email(
        self,
        email: str,
        template: str,
        subject: t.Optional[str] = None,
        variables: t.Optional[dict[str, t.Union[str, int]]] = None,
    ) -> None:
        """Отправляет email-сообщение"""

    def send_password_code(self, email: str, code: str) -> None:
        """Отправляет email-сообщение"""

    def send_password_change(self, email: str) -> None:
        """Отправляет email-сообщение"""

    def send_plan_change(self, email: str, tariff_name: str) -> None:
        """Отправляет email-сообщение"""

    def send_subs_cancel(self, email: str) -> None:
        """Отправляет email-сообщение"""

    def send_first_payment_greeting(
        self, email: str, tariff_period_days: int = 30
    ) -> None:
        """Отправляет email-сообщение"""

    def send_monthly_tariff_notification(self, email: str, date: str) -> None:
        """Отправляет email-сообщение"""

    def send_yearly_tariff_notification(self, email: str, date: str) -> None:
        """Отправляет email-сообщение"""

    def send_email_confirm_link(self, email: str, code: str) -> None:
        """Отправляет email-сообщение"""

    def send_email_nonactive_tariff_alert(
        self, email: str, user_name: str, tariff_name: str, take_down_date: str
    ) -> None:
        """Отправляет email-сообщение"""

    def send_email_nonactive_tariff_last_alert(
        self, email: str, user_name: str, tariff_name: str, take_down_date: str
    ) -> None:
        """Отправляет email-сообщение"""
