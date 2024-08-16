import os
import json
import appbuilder

from typing import Optional
from appbuilder.core.console.knowledge_base import data_class
from src.utils import progress


class AppBuilderKnowledgeBase:
    def __init__(self, base_type: str):
        with open('config/baidu.json', mode='r', encoding='utf-8') as f:
            config = json.load(f)

        os.environ['APPBUILDER_TOKEN'] = config['appbuilder_token']

        self.activated = bool(config['appbuilder_token'])
        self.knowledge_base: Optional[appbuilder.KnowledgeBase] = None

        if self.activated:
            self.knowledge_base = appbuilder.KnowledgeBase(config['knowledge_bases'][base_type])

    def compare_files_and_update(
        self,
        result: dict,
        separator: str = '\n\n',
    ):
        if not self.activated:
            return

        docs = {item.name: item for item in self.knowledge_base.get_all_documents()}

        for filename, item in progress(result.items(), 'updating knowledge_base'):
            if filename in docs:
                if docs[filename].word_count == item['length']:
                    continue
                self.knowledge_base.delete_document(docs[filename].id)

            upload_res = self.knowledge_base.upload_file(item['path'])

            self.knowledge_base.add_document(
                'raw_text',
                [upload_res.id],
                custom_process_rule=data_class.CustomProcessRule(
                    separators=['by_page'],
                    target_length=1200,
                    overlap_rate=0.25,
                ),
            )
