from typing import List, Dict, Optional
from src.baidu.bos import BosUploader
from src.utils import *


class OutputFiles:
    def __init__(
        self,
        out_dir: str,
        dist_folder: str = './dist',
        separator: str = '\n\n',
        uploader: Optional[BosUploader] = None,
        single_file: bool = False,
    ):
        if single_file:
            out_dir = f'{out_dir}-single'

        if os.path.exists(f'{dist_folder}/{out_dir}'):
            shutil.rmtree(f'{dist_folder}/{out_dir}')

        self.out_dir = out_dir
        self.dist_folder = dist_folder
        self.separator = separator
        self.uploader = uploader

        self.result = {}
        self.words_count = 0

        self.single_file = single_file
        self.single_file_contents: Dict[str, List[str]] = {}

    def __gen_file(self, name: str, path: str, content: str):
        count = len(content.replace('\n', '')) - 2

        self.result[f'{name}.txt'] = {
            'path': f'{self.dist_folder}/{path}',
            'length': count,
        }
        self.words_count += count

        if self.uploader:
            self.uploader.upload_string(f'/{path}', content)
        else:
            with create_file(f'{self.dist_folder}/{path}') as file:
                file.write(content)

    def create(self, name: str, group: str, contents: List[str]):
        content = self.separator.join(contents).strip('\n')

        if self.single_file:
            if group not in self.single_file_contents:
                self.single_file_contents[group] = []

            self.single_file_contents[group].append(f'《{name}》')
            self.single_file_contents[group].append(content)
            return

        self.__gen_file(
            name,
            f'{self.out_dir}/%s{name}.txt' % (f'{group}/' if group else ''),
            content,
        )

    def done(self):
        if self.single_file:
            for filename, contents in self.single_file_contents.items():
                content = self.separator.join(contents).strip('\n')
                self.__gen_file(
                    filename,
                    f'{self.out_dir}/{filename}.txt',
                    content,
                )

        print('文件数：', len(self.result.keys()))
        print('总字数：', self.words_count)

        with create_file(f'{self.dist_folder}/{self.out_dir}.json') as file:
            file.write(
                json.dumps(
                    self.result,
                    ensure_ascii=False,
                    indent=4,
                    separators=(',', ': '),
                )
            )
