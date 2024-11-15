import os
import json
import requests

from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
from src.utils import progress
from src.baidu.appBuilder.api import API


class AppBuilderKnowledgeBase:
    def __init__(self, base_type: str, new_base: bool = False):
        with open('config/baidu.json', mode='r', encoding='utf-8') as f:
            config = json.load(f)

        self.token = config['appbuilder_token']
        self.max_len = config['max_len']
        self.base_info = config['knowledge_bases'][base_type]
        self.base_name = self.base_info['name'] + (datetime.now().strftime('%Y%m%d') if new_base else '')
        self.knowledge_base_id = self.base_info['id']

        if not self.knowledge_base_id:
            self.create_base()

    @property
    def activated(self):
        return bool(self.token)

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

    def __post(self, url: str, payload: dict):
        response = requests.request('POST', url, headers=self.headers, data=json.dumps(payload))
        return json.loads(response.text)

    def get_all_bases(self, max_keys: int = 100):
        bases = {}
        marker = ''

        while True:
            res = self.__post(
                API.DescribeKnowledgeBases,
                {
                    'marker': marker,
                    'maxKeys': max_keys,
                },
            )

            bases.update({item['name']: item for item in res['data']})
            marker = res['nextMarker']

            if not res['isTruncated']:
                break

        return bases

    def create_base(self):
        bases = self.get_all_bases()

        if self.base_name in bases:
            self.knowledge_base_id = bases[self.base_name]['id']
            return

        res = self.__post(
            API.CreateKnowledgeBase,
            {
                'name': self.base_name,
                'description': self.base_info['desc'],
                'config': {
                    'index': {
                        'type': 'public',
                    }
                },
            },
        )
        self.knowledge_base_id = res['id']

    def get_all_documents(self, max_keys: int = 100):
        docs = {}
        marker = None

        while True:
            res = self.__post(
                API.DescribeDocuments,
                {
                    'knowledgeBaseId': self.knowledge_base_id,
                    'marker': marker,
                    'maxKeys': max_keys,
                },
            )

            docs.update({item['name']: item for item in res['data']})
            marker = res['nextMarker']

            if not res['isTruncated']:
                break

        return docs

    def add_document(self, path: str, separator: str = '\n\n', max_len: int = 8000, overlap_rate: float = 0.25):
        files = {
            'file': (os.path.basename(path), open(path, 'rb')),
            'payload': json.dumps(
                {
                    'id': self.knowledge_base_id,
                    'source': {
                        'type': 'file',
                    },
                    'contentFormat': 'rawText',
                    'processOption': {
                        'template': 'custom',
                        'chunker': {
                            'choices': ['pattern'],
                            'pattern': {
                                'markPosition': 'tail',
                                'regex': separator,
                                'targetLength': max_len,
                                'overlapRate': overlap_rate,
                            }
                        },
                    },
                }
            ),
        }
        payload = MultipartEncoder(fields=files)
        response = requests.post(
            API.UploadDocuments,
            data=payload,
            headers={
                'Content-Type': payload.content_type,
                'Authorization': f'Bearer {self.token}',
            },
        )
        return json.loads(response.text)

    def delete_document(self, doc_id: str):
        res = self.__post(
            API.DeleteDocument,
            {
                'knowledgeBaseId': self.knowledge_base_id,
                'documentId': doc_id,
            },
        )
        return res

    def compare_files_and_update(
        self,
        result: dict,
        separator: str = '\n\n',
    ):
        if not self.activated:
            return

        docs = self.get_all_documents()

        for filename, item in progress(result.items(), 'updating knowledge_base'):
            if filename in docs:
                doc = docs[filename]
                if doc['wordCount'] == item['length']:
                    continue
                self.delete_document(doc['id'])

            self.add_document(item['path'], separator=separator, max_len=self.max_len)
