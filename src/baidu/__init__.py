from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration


class BosUploader:
    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        bos_host: str = 'gz.bcebos.com',
        bucket_name: str = '',
    ):
        config = BceClientConfiguration(
            credentials=BceCredentials(access_key_id, secret_access_key),
            endpoint=bos_host,
        )
        self.bos_client = BosClient(config)
        self.bucket_name = bucket_name or self.bos_client.list_buckets().buckets[0].name

    def upload_string(self, object_key: str, text: str):
        self.bos_client.put_object_from_string(self.bucket_name, object_key, text)

    def upload_file(self, object_key: str, file_name: str):
        self.bos_client.put_object_from_file(self.bucket_name, object_key, file_name)
