from pathlib import Path
import json
import time
import sys

import speech_recognition as sr
from tqdm import tqdm

from pafts.datasets.dataset import Dataset

STT_API_LIST = [
    'google_web_speech',
    'google_cloud_stt',
    'azure_stt'
]


def read_key(key_path: str, stt_api_name: str):
    """
    Read the key file and return the key value corresponding to the api.
    The key file is json file.

    Args:
        key_path (str): key file path.
        stt_api_name (str): Name of STT API to use

    Return:
        If api name is google_cloud_stt, return {'key' : '', 'location' : ''}.
        If api name is azure_stt, return credentials_json file path

    """
    if not Path(key_path).exists() or not key_path:
        raise Exception('[!] Key path is not correct!')

    with open(key_path, 'r', encoding="utf-8") as f:
        key = json.load(f)

    if stt_api_name not in key or not key[stt_api_name]:
        raise Exception(f'[!] The api key for {stt_api_name} does not exist!')

    return key[stt_api_name]


def google_web_speech(
        dataset: Dataset,
        abs_path: bool = False

):
    """
    Get text values for audio files using Google Web Speech Api and Return key-value pairs
    This api is free, and you don't need to get a key.
    However, there is a limit to the number of times you can use it per day.

    Args:
        dataset (Dataset): Dataset.
        abs_path (bool):
            The shape of the key of the return value dict.
            False is only file name, True is absolute path
            Defaults to False.

    Returns:
        Dict:
            Audio file and text pairs.
            example
                {
                    '1_001.wav' : "I have a note.",
                    '1_002.wav' : "I want to eat chicken."
                    }

    """
    print(f'> Preparing STT API...')
    print(f'| > STT API : google web speech')
    dataset.print_info()

    time.sleep(1)
    items = dataset.get_audio_file()
    stt_dict = {}

    r = sr.Recognizer()

    bar = tqdm(items,
               total=len(items),
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        text = ''

        with sr.AudioFile(str(item)) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio_data=audio, language=dataset.language)
        except sr.UnknownValueError:
            text = None
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")

        bar.set_description(f'{item.name}')

        if abs_path:
            stt_dict[str(item)] = text
        else:
            stt_dict[item.name] = text

    print()

    return stt_dict


def google_cloud_stt(
        dataset: Dataset,
        key_path: str,
        abs_path: bool = False,

):
    """
    Get text values for audio files using Google Cloud STT Api and Return key-value pairs

    This api is available for free for one hour a month.
    Please be careful because you may be charged if you exceed one hour.
    For more information about pricing, please check the link below
    https://cloud.google.com/speech-to-text/pricing

    The api key is required to use this function.
    Check the link below for information on how to receive the API key
    https://cloud.google.com/speech-to-text

    Args:
        dataset (Dataset): Dataset.
        key_path (str): Path to the json file containing the API key.
        abs_path (bool):
            The shape of the key of the return value dict.
            False is only file name, True is absolute path
            Defaults to False.

    Returns:
        Dict:
            Audio file and text pairs.
            example
                {
                    '1_001.wav' : "I have a note.",
                    '1_002.wav' : "I want to eat chicken."
                    }

    """
    print(f'> Preparing STT API...')
    print(f'| > STT API : Google Cloud STT')
    dataset.print_info()

    time.sleep(1)
    items = dataset.get_audio_file()
    stt_dict = {}

    r = sr.Recognizer()
    key = read_key(key_path, 'google_cloud_stt')

    bar = tqdm(items,
               total=len(items),
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        text = ''

        with sr.AudioFile(str(item)) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google_cloud(
                audio_data=audio,
                language=dataset.language,
                credentials_json=key

            )
        except sr.UnknownValueError:
            text = None
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Microsoft Azure Speech service; {e}")

        bar.set_description(f'{item.name}')

        if abs_path:
            stt_dict[str(item)] = text
        else:
            stt_dict[item.name] = text

    print()

    return stt_dict


def azure_stt(
        dataset: Dataset,
        key_path: str,
        abs_path: bool = False,

):
    """
    Get text values for audio files using Microsoft Azure Speech Api and Return key-value pairs

    This api is available for free for 5 hours a month.
    Please be careful because you may be charged if you exceed 5 hours.
    For more information about pricing, please check the link below
    https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/

    The api key is required to use this function.
    Check the link below for information on how to receive the API key
    https://azure.microsoft.com/products/cognitive-services/speech-to-text/

    Args:
        dataset (Dataset): Dataset.
        key_path (str): Path to the json file containing the API key.
        abs_path (bool):
            The shape of the key of the return value dict.
            False is only file name, True is absolute path
            Defaults to False.

    Returns:
        Dict:
            Audio file and text pairs.
            example
                {
                    '1_001.wav' : "I have a note.",
                    '1_002.wav' : "I want to eat chicken."
                    }

    """
    print(f'> Preparing STT API...')
    print(f'| > STT API : Microsoft Azure Speech')
    dataset.print_info()

    time.sleep(1)
    items = dataset.get_audio_file()
    stt_dict = {}

    r = sr.Recognizer()
    key = read_key(key_path, 'azure_stt')

    bar = tqdm(items,
               total=len(items),
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        text = ''

        with sr.AudioFile(str(item)) as source:
            audio = r.record(source)

        try:
            # return shape => (text, predict)
            text = r.recognize_azure(
                audio_data=audio,
                language=dataset.language,
                key=key['key'],
                location=key['location']
            )
        except sr.UnknownValueError:
            text = None
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Microsoft Azure Speech service; {e}")

        bar.set_description(f'{item.name}')

        if abs_path:
            stt_dict[str(item)] = text[0]
        else:
            stt_dict[item.name] = text[0]

    print()

    return stt_dict
