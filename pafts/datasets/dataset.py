from pathlib import Path

from pydub import AudioSegment

"""Supported Audio formats"""
AUDIO_FORMATS = [
    'wav',
    'mp3',
    'ogg',
    'flac'
]


def is_audio(path):
    file = Path(path)
    if file.suffix[1:] in AUDIO_FORMATS:
        return True
    return False


def get_duration(path):
    audio = AudioSegment.from_file(path)
    return audio.duration_seconds


class Dataset:
    """
    Audio Dataset Class.
    Process all audio data class.

    Args:
        path (str): Directory path with audio files.
        dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
        language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)
        output_path (str): Output Directory. Defaults to './pafts_output'

    """

    def __init__(
            self,
            path: str = None,
            dataset_name: str = None,
            language: str = None,
            output_path: str = 'pafts_output'
    ):

        self._path = Path(path).resolve()
        self._output_path = Path(output_path)
        self._dataset_name = dataset_name
        self._language = language
        self._audios = []

        if not self._path.exists():
            raise FileNotFoundError("[!] Path does not exist")

        if not self._path.is_dir():
            raise NotADirectoryError("[!] Path is not directory.")

        if not self._dataset_name:
            self._dataset_name = self._path.name

        if not self._output_path.exists():
            self._output_path.mkdir(parents=True)

        # find audio file in path
        # self._audios = [Data(str(p)) for p in self._path.glob("**/*") if is_audio(p)]
        self._audios = [Path(p) for p in self._path.glob("**/*") if is_audio(p)]

    def __len__(self):
        return len(self._audios)

    def __getitem__(self, index):
        return self._audios[index]

    @property
    def audios(self):
        return self._audios

    @audios.setter
    def audios(self, audios):
        if isinstance(audios, list) and all(isinstance(audio, Path) for audio in audios):
            self._audios = audios
        else:
            raise ValueError("[!] The input value is not a list or the element in the list is not a Path type.")

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def output_path(self):
        return self._output_path

    @property
    def path(self):
        return self._path

    @output_path.setter
    def output_path(self, output_path):
        if (isinstance(output_path, str) or isinstance(output_path, Path)) and Path(output_path).exists():
            self._output_path = output_path
        else:
            raise ValueError("[!] The input is wrong.")

    @path.setter
    def path(self, path):
        if (isinstance(path, str) or isinstance(path, Path)) and Path(path).exists():
            self._path = path
            self._audios = [Path(p) for p in self._path.glob("**/*") if is_audio(p)]
        else:
            raise ValueError("[!] The input is wrong.")

    def print_info(self):
        print(f'| > Dataset name : {self._dataset_name}')
        print(f'| > Path : {self._path}')
        print(f'| > language : {self._language}')
        print(f'| > Number of files : {len(self._audios)}')
        print(f'| > Total duration : {self.get_total_duration()}')

    def get_total_duration(self):
        total_duration = 0

        for audio in self._audios:
            total_duration += get_duration(audio)
        return total_duration
