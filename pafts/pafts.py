from pathlib import Path
import json

from pafts.datasets.dataset import Dataset
from pafts.utils.transform import change_sr, change_channel, change_format
from pafts.cleaner.delete_bgm import delete_bgm
from pafts.stt.stt_apis import google_web_speech, google_cloud_stt, azure_stt, STT_API_LIST
from pafts.utils.file_utils import save_dict, delete_none_value


class PAFTS:
    """
        Make audio files into a dataset for TTS.

        Args:
            dataset_path (str): Directory path with audio files.
            language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)
            dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
            key_path (str, optional):
                STT API key path. If you use the API that requires a key, you must enter it. (key is json file)
                Defaults to None.

        Example with quick start:
            >>> from pafts.pafts import PAFTS
            >>> pafts = PAFTS(dataset_path="your dataset path", language='language')
            >>> pafts.run()

        If you want to task step by step:
            >>> from pafts.pafts import PAFTS
            >>> pafts = PAFTS(dataset_path="your dataset path", language='language', dataset_name='dataset name', key_path='api key path')
            >>> pafts.transform_items(sr=22050, channel=1, formats='audio format')
            >>> pafts.delete_bgm()
            >>> dic = pafts.stt(stt_api_name='stt api name')
            >>> pafts.save(dic=dic, file_name='text.json')

        """

    def __init__(
            self,
            dataset_path: str,
            language: str = 'en-us',
            dataset_name: str = None,
            key_path: str = None
    ):
        self.dataset = Dataset(
            path=dataset_path,
            dataset_name=dataset_name,
            language=language
        )

        self.key_path = key_path

    def flatten(self):
        """Flatten directory structure."""
        print(f'> Flatten directory structure.')
        print()
        self.dataset.flatten()

    def transform_items(self, sr: int = 22050, channel: int = 1, formats: str = 'wav'):
        """
        Change sampling rate, channel, format

        Args:
            sr (int, optional): Audio file's sampling rate. Defaults to 22050.
            channel (int, optional): Audio file's channel. Defaults to 1.
            formats (str, optional): Audio file's format. Defaults to 'wav'.
        """

        print(f'> Transform items...')
        print(f'| > sr : {sr}')
        print(f'| > channel : {channel}')
        print(f'| > format : {formats}')
        change_sr(self.dataset, sr=sr)
        change_channel(self.dataset, channel=channel)
        change_format(self.dataset, formats=formats)
        print()

    def delete_bgm(self, multiprocess: bool = False):
        """
        Delete BGM from audio file

        Args:
            multiprocess (bool): Multiprocessing Delete BGM. Defaults to False.
        """

        delete_bgm(self.dataset, multiprocess=multiprocess)

    def stt(self, stt_api_name: str = 'google_web_speech', abs_path: bool = False):
        """
        Get text values for audio files using STT API and Return key-value pairs.

        Args:
            stt_api_name (str, optional): Name of the api to use. Defaults to 'google_web_speech'.
            abs_path (bool, optional):
                The shape of the key of the return value dict.
                False is only file name, True is absolute path.
                Defaults to False.

        Return:
            Dict: Audio file and text pairs.
        """

        if stt_api_name not in STT_API_LIST:
            raise Exception(
                '[!] Unsupported api. Please choose one of these.\n google_web_speech, azure_stt, google_cloud_stt')
        elif stt_api_name == 'google_web_speech':
            return google_web_speech(self.dataset)
        elif stt_api_name == 'google_cloud_stt':
            return google_cloud_stt(dataset=self.dataset, key_path=self.key_path, abs_path=abs_path)
        elif stt_api_name == 'azure_stt':
            return azure_stt(dataset=self.dataset, key_path=self.key_path, abs_path=abs_path)

    def save(self, dic: dict, file_name: str = 'text.json', delete_none: bool = True):
        """
        Save the dict as a json file.

        Args:
            dic (dict): Audio file and text pairs.
            file_name (str, optional): Output text file name. Defaults to 'text.json'.
            delete_none (bool, optional): Delete the none value of the dic. Defaults to True.
        """
        if delete_none:
            dic = delete_none_value(path=self.dataset.path, dic=dic)

        save_dict(path=self.dataset.path, dic=dic, file_name=file_name)

    def check_args(self, stt_api_name: str):
        """
        Check three cases.
            1. Does an audio file exist?
            2. Does it support selected STT_API?
            3. If the selected STT_API requires a key, does the key exist?

        Args:
            stt_api_name (str): Name of the speech to text api to use
        """
        if self.dataset.get_file_num() < 1:
            raise Exception('[!] Audio file does not exist.')

        if stt_api_name not in STT_API_LIST:
            raise Exception(
                '[!] Unsupported api. Please choose one of these.\n google_web_speech, azure_stt, google_cloud_stt')

        if stt_api_name != 'google_web_speech':
            if not self.key_path:
                raise Exception('[!] Key path does not exist!')

            if not Path(self.key_path).exists():
                raise Exception('[!] Key path is not correct!')

            with open(self.key_path, 'r', encoding="utf-8") as f:
                key = json.load(f)

            if stt_api_name not in key or not key[stt_api_name]:
                raise Exception(f'[!] The api key for {stt_api_name} does not exist!')

    def run(
            self,
            flat: bool = False,
            sr: int = 22050,
            channel: int = 1,
            formats: str = 'wav',
            multiprocess: bool = False,
            stt_api_name: str = 'google_web_speech',
            file_name: str = 'text.json',
            delete_none: bool = True

    ):
        """
        Make audio files into a dataset for TTS.

        Process.
            1. Transform items.
            2. Delete BGM.
            3. STT. (Create audio and text pairs)
            4. Save dict.

        Args:
            flat (bool, optional): Flatten directory structure. Defaults to False.
            sr (int, optional): Audio file's sampling rate. Defaults to 22050.
            channel (int, optional): Audio file's channel. Defaults to 1.
            formats (str, optional): Audio file's format. Defaults to 'wav'.
            multiprocess (bool): Multiprocessing Delete BGM. Defaults to False.
            stt_api_name (str, optional): Name of the speech to text api to use. Defaults to 'google_web_speech'.
            file_name (str, optional): Output text file name. Defaults to 'text.json'.
            delete_none (bool, optional): Delete the none value of the dic. Defaults to True.
        """
        print('>> Run...')

        self.dataset.print_info()

        self.check_args(stt_api_name)

        if flat:
            self.flatten()

        self.transform_items(sr, channel, formats)

        self.delete_bgm(multiprocess=multiprocess)

        dic = self.stt(stt_api_name=stt_api_name)

        self.save(dic=dic, file_name=file_name, delete_none=delete_none)

        print('Successfully Completed.')
