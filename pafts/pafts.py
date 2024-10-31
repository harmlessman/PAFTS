from pathlib import Path
import uuid
from datetime import datetime

from pafts.datasets.dataset import Dataset
from pafts.utils.transform import change_sr, change_channel, change_format
from pafts.diarization.diarization import diarization
from pafts.separator.separator import separator
from pafts.stt.stt import STT

class PAFTS:
    """
        Make audio files into a dataset for TTS.

        Args:
        path (str): Directory path with audio files.
        dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
        language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)
        output_path (str): Output Directory. Defaults to './pafts_output'

        Example with quick start:


        If you want to task step by step:



        """

    def __init__(
            self,
            path: str = None,
            dataset_name: str = None,
            language: str = None,
            output_path: str = 'pafts_output',
            hf_token: str = None
    ):

        self._hf_token = hf_token

        self._dataset = Dataset(
            path=path,
            dataset_name=dataset_name,
            language=language,
            output_path=output_path
        )

    def transform_items(self, formats: str = 'wav', sr: int = 22050, channel: int = 1):
        """
        Change format, sampling rate, channel

        Args:
            formats (str, optional): Audio file's format. Defaults to 'wav'.
            sr (int, optional): Audio file's sampling rate. Defaults to 22050.
            channel (int, optional): Audio file's channel. Defaults to 1.
        """

        print(f'> Transform items...\n| > format : {formats}\n| > sr : {sr}\n| > channel : {channel}')

        change_format(self.dataset, formats=formats)
        change_sr(self.dataset, sr=sr)
        change_channel(self.dataset, channel=channel)
        print()\


    def separator(self):
        separator(self._dataset)
        return

    def diarization(self):
        if not self._hf_token:
            raise TypeError("[!] Hugging Face access token is required to use diarization model.")

        diarization(self._dataset, self._hf_token)

        return

    def stt(self, output_format='json', model_size='large'):
        STT(self._dataset, output_format=output_format, model_size=model_size)
        return

    def run(self):
        # 1stage, separator
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex

        temp_dir = Path.cwd() / f"temp_dir_{timestamp}_{unique_id}"
        temp_dir.mkdir(exist_ok=True)

        self._dataset.output_path = temp_dir
        separator(self._dataset)
        self._dataset.path = temp_dir

        # 2stage, diarization
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex

        temp_dir = Path.cwd() / f"temp_dir_{timestamp}_{unique_id}"
        temp_dir.mkdir(exist_ok=True)

        self._dataset.output_path = temp_dir
        diarization(self._dataset, hf_token=self._hf_token)
        self._dataset.path = temp_dir

        # 3stage, stt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex

        temp_dir = Path.cwd() / f"temp_dir_{timestamp}_{unique_id}"
        temp_dir.mkdir(exist_ok=True)

        self._dataset.output_path = temp_dir
        STT(self._dataset)

