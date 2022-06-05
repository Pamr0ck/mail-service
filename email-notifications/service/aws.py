import requests
import boto3
import logging
import os

from service.lockbox import LockBox

logging.getLogger().setLevel(logging.INFO)

lockbox = LockBox()

secret_id = os.environ['LOCKBOX_SA_KEY_ID']
sa_credentials = lockbox[secret_id]


async def send_message_to_dlq(
        body: str
) -> None:
    client = boto3.session.Session(
        aws_access_key_id=sa_credentials['ACCESS_KEY_ID'],
        aws_secret_access_key=sa_credentials['SECRET_ACCESS_KEY'],
        region_name='ru-central1'
    ).client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
    )
    queue_url = client.get_queue_url(QueueName='email-notifications-queue')

    response = client.send_message(
        QueueUrl=queue_url['QueueUrl'],
        MessageBody=body
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != requests.codes.ok:
        logging.error(
            response.text
        )
    else:
        logging.info("message sent")
