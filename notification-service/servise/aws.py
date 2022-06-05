import requests
import aioboto3
import json
import logging
import os

from configuration.lockbox import LockBox

logging.getLogger().setLevel(logging.INFO)

lockbox = LockBox()

secret_id = os.environ['LOCKBOX_SA_KEY_ID']
sa_credentials = lockbox[secret_id]


async def send_message_to_sqs(
        email: str,
        template: str,
        text: str = '',
        subject: str = '',
        variable: str = '',
) -> None:
    session = aioboto3.Session()
    async with session.client(
            service_name='sqs',
            endpoint_url='https://message-queue.api.cloud.yandex.net',
            region_name='ru-central1',
            aws_access_key_id=sa_credentials['ACCESS_KEY_ID'],
            aws_secret_access_key=sa_credentials['SECRET_ACCESS_KEY']
    ) as client:
        json_data = {
            "to": email,
            "subject": subject,
            "text": text,
            "template": template,
            "variable": variable
        }

        queue_url = await client.get_queue_url(QueueName='email-notifications-queue')
        logging.info('get queue url is "{}"'.format(queue_url))

        response = await client.send_message(
            QueueUrl=queue_url['QueueUrl'],
            MessageBody=json.dumps(json_data)
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != requests.codes.ok:
            logging.error(
                response.text
            )
        else:
            logging.info("message sent")
