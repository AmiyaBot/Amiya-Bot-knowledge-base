from baidubce.services.bos.bos_client import BosClient


def upload_string(bos_client: BosClient, bucket_name: str, object_key: str, text: str):
    bos_client.put_object_from_string(bucket_name, object_key, text)


def upload_file(bos_client: BosClient, bucket_name: str, object_key: str, file_name: str):
    bos_client.put_object_from_file(bucket_name, object_key, file_name)
