from pathlib import Path

import numpy as np
import torch
from pydub import AudioSegment

from pafts.utils.data_info import is_audio


class Data:
    """
    Audio Data Class.

    Args:
        file_path (str): File path with audio files.
    """

    def __init__(
            self,
            file_path: str
    ):
        self.sr = None
        self.channels = None
        self.audio_data = None
        self.duration = None
        self._name = Path(file_path).name

        audio = AudioSegment.from_file(file_path)

        self.sr = audio.frame_rate
        self.channels = audio.channels

        # 오디오 데이터를 numpy 배열로 변환
        audio = np.array(audio.get_array_of_samples())

        # 데이터 정규화 (16-bit PCM 데이터를 float32로 변환)
        audio = audio.astype(np.float32) / 32768.0
        audio = torch.from_numpy(audio)

        self.audio_data = audio

        self.duration = self.audio_data.shape[0] / self.sr

    def set_sample_rate(self, sr):
        self.sr = sr

    def set_channels(self, channels):
        self.channels = channels

    def save_audio(self, output_path: str, format: str = 'wav'):
        audio_np = self.audio_data.numpy()

        # 데이터 역정규화 (float32 데이터를 16-bit PCM으로 변환)
        audio_np = (audio_np * 32768.0).astype(np.int16)

        audio = AudioSegment(
            audio_np.tobytes(),
            frame_rate=self.sr,
            channels=self.channels,
        )
        audio.export(output_path, format=format)

    @property
    def name(self):
        return self._name


class Dataset:
    """
    Audio Dataset Class.
    Process all audio data class.

    Args:
        path (str): Directory path with audio files.
        dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
        language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)

    """

    def __init__(
            self,
            path: str = None,
            dataset_name: str = None,
            language: str = None,
    ):

        self._path = Path(path).resolve()
        self._dataset_name = dataset_name
        self._language = language
        self._audios = []

        if not self._path.exists():
            raise FileNotFoundError("[!] Path does not exist")

        if not self._path.is_dir():
            raise NotADirectoryError("[!] Path is not directory.")

        if not self._dataset_name:
            self._dataset_name = self._path.name

        # find audio file in path
        self._audios = [Data(str(p)) for p in self._path.glob("**/*") if is_audio(p)]

    def __len__(self):
        return len(self._audios)

    def __getitem__(self, index):
        return self._audios[index]

    @property
    def audios(self):
        return self._audios

    @property
    def dataset_name(self):
        return self._dataset_name

    def print_info(self):
        print(f'| > Dataset name : {self._dataset_name}')
        print(f'| > Path : {self._path}')
        print(f'| > language : {self._language}')
        print(f'| > Number of files : {len(self._audios)}')
        print(f'| > Total duration : {self.get_total_duration()}')

    def get_total_duration(self):
        total_duration = 0

        for audio in self._audios:
            total_duration += audio.duration
        return total_duration

