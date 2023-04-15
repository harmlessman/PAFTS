from pathlib import Path

from PAFTS.utils.data_info import is_audio, get_duration
from PAFTS.utils.file_utils import rmtree


class Dataset:
    """
    Audio Dataset Class.
    Process all audio files in path.

    Args:
        path (str): Directory path with audio files.
        dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
        language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)

    """
    def __init__(
            self,
            path: str,
            dataset_name: str = None,
            language: str = "en-us",

    ):
        if not Path(path).exists():
            raise FileNotFoundError("[!] Path does not exist")

        if not Path(path).is_dir():
            raise NotADirectoryError("[!] Path is not directory.")

        self.path = Path(path)

        if dataset_name:
            self.dataset_name = dataset_name
        else:
            self.dataset_name = Path(path).name

        self.language = language

    def get_audio_file(self):
        return [p for p in self.path.glob("**/*") if is_audio(p)]

    def get_total_duration(self):
        total_duration = 0
        items = self.get_audio_file()

        for item in items:
            total_duration += get_duration(item)
        return total_duration

    def get_file_num(self):
        return len(self.get_audio_file())

    def __len__(self):
        return self.get_file_num()

    def flatten(self):
        """
        Flatten directory structure.

        Example :

            before dataset structure

              path
                ├── a
                │   ├── 1.wav
                │   ├── 2.wav
                │   └── 3.wav
                ├── b
                │   ├── 1.wav
                │   └── 2.wav
                ├── 1.wav
                ├── 2.wav
                └── c
                    └── d
                        └── 1.wav

            after dataset structure

                  path
                    ├── a_1.wav
                    ├── a_2.wav
                    ├── a_3.wav
                    ├── b_1.wav
                    ├── b_2.wav
                    ├── 1.wav
                    ├── 2.wav
                    └── c_d_1.wav

        """
        items = self.get_audio_file()

        for item in items:
            p = item.parent
            if p.samefile(self.path):
                name = item.name
            else:
                front_list = str(p.relative_to(self.path)).split('\\')
                name = '_'.join((front_list + [item.name]))

            item.rename(self.path / name)

        # remove empty directory
        dir_list = [i for i in self.path.glob('*') if i.is_dir()]

        for d in dir_list:
            rmtree(d)

    def print_info(self):
        print(f'| > Dataset name : {self.dataset_name}')
        print(f'| > Path : {self.path}')
        print(f'| > language : {self.language}')
        print(f'| > Number of files : {self.get_file_num()}')
        print(f'| > Total duration : {self.get_total_duration()}')
        print()
