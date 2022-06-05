from pydantic import BaseModel, Json
from notifications.stubs.default_categories import NotificationCategory
import typing as t


class CreateRequest(BaseModel):
    target_user_id: str
    category: NotificationCategory
    payload: Json


class ReadRequest(BaseModel):
    ids: t.List[str]


class SendNotificationRequest(BaseModel):
    email: str
    category: NotificationCategory
    payload: str


class SendPasswordCodeRequest(BaseModel):
    email: str
    code: str


class SendPasswordChangeRequest(BaseModel):
    email: str


class SendPlanChangeRequest(BaseModel):
    email: str
    tariff_name: str


class SendSubsCancel(BaseModel):
    email: str


class SendFirstPaymentGreeting(BaseModel):
    email: str
    tariff_period_days: int


class SendMonthlyTariffNotification(BaseModel):
    email: str
    date: str


class SendYearlyTariffNotification(BaseModel):
    email: str
    date: str


class SendEmailConfirmLink(BaseModel):
    email: str
    code: str


class SendEmailNonactiveTariff(BaseModel):
    email: str
    take_down_date: str


class SendEmailNonactiveTariffLastAlert(BaseModel):
    email: str
    take_down_date: str


class AnswerCode(BaseModel):
    status: str
    success: bool
