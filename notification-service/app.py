from fastapi import FastAPI

from notifications.notification import Notification
from payloads import (CreateRequest,
                      ReadRequest,
                      AnswerCode,
                      SendNotificationRequest,
                      SendPasswordCodeRequest,
                      SendPasswordChangeRequest,
                      SendPlanChangeRequest,
                      SendMonthlyTariffNotification,
                      SendEmailNonactiveTariffLastAlert,
                      SendFirstPaymentGreeting,
                      SendYearlyTariffNotification,
                      SendEmailNonactiveTariff,
                      SendEmailConfirmLink,
                      SendSubsCancel)

app = FastAPI()


@app.put('/make_notification_read')
async def make_notification_read(request: ReadRequest):
    notifications_count = await Notification.make_notification_read(
        notification_ids=request.ids
    )
    return {
        "data": notifications_count,
    }


@app.post('/create_notification', response_model=AnswerCode)
async def create_notification(request: CreateRequest):
    notification_id = await Notification.create_notification(
        target_user_id=request.target_user_id,
        category=request.category,
        payload=request.payload
    )
    return {
        "status": notification_id,
        "success": True
    }


@app.post('/send_new_notification', response_model=AnswerCode)
async def send_password_code(request: SendNotificationRequest):
    code = await Notification.create_notification(
        target_user_id=request.target_user_id,
        category=request.category,
        payload=request.payload
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_password_code', response_model=AnswerCode)
async def send_password_code(request: SendPasswordCodeRequest):
    code = await Notification.send_password_code(
        email=request.email,
        code=request.code
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_password_change', response_model=AnswerCode)
async def send_password_change(request: SendPasswordChangeRequest):
    code = await Notification.send_password_change(
        email=request.email,
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_plan_change', response_model=AnswerCode)
async def send_plan_change(request: SendPlanChangeRequest):
    code = await Notification.send_plan_change(
        email=request.email,
        tariff_name=request.tariff_name
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_subs_cancel', response_model=AnswerCode)
async def send_subs_cancel(request: SendSubsCancel):
    code = await Notification.send_subs_cancel(
        email=request.email
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_first_payment_greeting', response_model=AnswerCode)
async def send_first_payment_greeting(request: SendFirstPaymentGreeting):
    code = await Notification.send_first_payment_greeting(
        email=request.email,
        days=request.tariff_period_days
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_monthly_tariff_notification', response_model=AnswerCode)
async def send_monthly_tariff_notification(request: SendMonthlyTariffNotification):
    code = await Notification.send_monthly_tariff_notification(
        email=request.email,
        date=request.date
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_yearly_tariff_notification', response_model=AnswerCode)
async def send_yearly_tariff_notification(request: SendYearlyTariffNotification):
    code = await Notification.send_yearly_tariff_notification(
        email=request.email,
        date=request.date
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_email_confirm_link', response_model=AnswerCode)
async def send_email_confirm_link(request: SendEmailConfirmLink):
    code = await Notification.send_email_confirm_link(
        email=request.email,
        code=request.code
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_email_nonactive_tariff_alert', response_model=AnswerCode)
async def send_email_nonactive_tariff_alert(request: SendEmailNonactiveTariff):
    code = await Notification.send_email_nonactive_tariff_alert(
        email=request.email,
        date=request.take_down_date
    )
    return {
        "success": True,
        "status": code
    }


@app.post('/send_email_nonactive_tariff_last_alert', response_model=AnswerCode)
async def send_email_nonactive_tariff_last_alert(request: SendEmailNonactiveTariffLastAlert):
    code = await Notification.send_email_nonactive_tariff_last_alert(
        email=request.email,
        date=request.take_down_date
    )
    return {
        "success": True,
        "status": code
    }
