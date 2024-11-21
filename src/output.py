from typing import List, Dict, Optional
from src.utils import *


class OutputFiles:
    def __init__(
        self,
        out_dir: str,
        dist_folder: str = './dist',
        separator: str = '\n\n',
        single_file: bool = False,
        single_file_group: bool = False,
        single_file_group_max: int = 100,
    ):
        if single_file:
            out_dir = f'{out_dir}-single'

        if os.path.exists(f'{dist_folder}/{out_dir}'):
            shutil.rmtree(f'{dist_folder}/{out_dir}')

        self.out_dir = out_dir
        self.dist_folder = dist_folder
        self.separator = separator

        self.result = {}
        self.words_count = 0

        self.single_file = single_file
        self.single_file_group = single_file_group
        self.single_file_group_max = single_file_group_max
        self.single_file_contents: Dict[str, List[str]] = {}

    def __gen_file(self, name: str, path: str, content: str, extra: Optional[dict] = None):
        # count = len(content.replace('\n', '')) - 2
        count = len(content)

        self.result[f'{name}.txt'] = {
            'path': f'{self.dist_folder}/{path}',
            'length': count,
            'extra': (extra or {}),
        }
        self.words_count += count

        with create_file(f'{self.dist_folder}/{path}') as file:
            file.write(content)

    def create(self, name: str, group: str, contents: List[str], extra: Optional[dict] = None):
        content = self.separator.join(contents).strip('\n')

        if self.single_file:
            if group not in self.single_file_contents:
                self.single_file_contents[group] = []

            # self.single_file_contents[group].append(f'《{name}》\n\n{content}')
            self.single_file_contents[group].append(content)
            return

        self.__gen_file(name, f'{self.out_dir}/%s{name}.txt' % (f'{group}/' if group else ''), content, extra)

    def done(self):
        if self.single_file:
            rec = 0
            index = 1

            for filename, contents in self.single_file_contents.items():
                out_dir = f'{self.out_dir}/{index}' if self.single_file_group else self.out_dir
                content = self.separator.join(contents).strip('\n')
                self.__gen_file(
                    filename,
                    f'{out_dir}/{filename}.txt',
                    content,
                )

                if self.single_file_group:
                    rec += 1
                    if rec >= self.single_file_group_max:
                        index += 1
                        rec = 0

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
