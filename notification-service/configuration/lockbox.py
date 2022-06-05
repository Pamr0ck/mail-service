import typing as t

import yandexcloud
from yandex.cloud.lockbox.v1.payload_service_pb2 import GetPayloadRequest
from yandex.cloud.lockbox.v1.payload_service_pb2_grpc import PayloadServiceStub


class LockBox:
    def __init__(self) -> None:
        yc_sdk = yandexcloud.SDK()
        channel = yc_sdk._channels.channel("lockbox-payload")
        self.lockbox = PayloadServiceStub(channel)

    def __getitem__(self, secret_id: str) -> t.Dict[str, t.Any]:
        response = self.lockbox.Get(GetPayloadRequest(secret_id=secret_id))
        entries = {}

        for entry in response.entries:
            entries[entry.key] = entry.text_value

        return entries
