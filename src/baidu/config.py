from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration


def create_config(
    access_key_id: str,
    secret_access_key: str,
    bos_host: str = 'gz.bcebos.com',
):
    return BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)


def init_client(
    access_key_id: str,
    secret_access_key: str,
    bos_host: str = 'gz.bcebos.com',
):
    return BosClient(create_config(access_key_id, secret_access_key, bos_host))
