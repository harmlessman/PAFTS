import json
from pathlib import Path

import whisper
from whisper.tokenizer import LANGUAGES
from tqdm import tqdm

from pafts.datasets.dataset import Data, Dataset

whisper_model = {
    "tiny": None,
    "base": None,
    "small": None,
    "medium": None,
    "large": None
}


def whisper_stt(
        data: Data,
        model_size='base',
        language=None,
):
    """
        Use the Whipser[https://github.com/openai/whisper] STT model to extract text.
        If there is no gpu or low performance, use the base model.

        Args:
            data (Data): Audio data.
            model_size (str): Size of the whisper model.
            language (str): Language of the audio file to run STT.

        Return:
            str: Text in an audio file.

        """
    global whisper_model
    if model_size not in whisper_model.keys():
        raise ValueError(
            "[!] Invalid model size selected. Please choose one of the following sizes: tiny, base, small, medium, large.")

    if not whisper_model[model_size]:
        whisper_model[model_size] = whisper.load_model(model_size)

    if language and language not in LANGUAGES:
        raise ValueError(
            f"[!] This language is not supported. Please select one of the language codes below\n{LANGUAGES}")

    result = whisper_model[model_size].transcribe(data.audio_data)

    return result['text']


def STT(
        dataset: Dataset,
        output_path: str,
        model_size='base',
        language=None
):
    """
    Read the audio files in the dataset, and use the stt function to extract text.
    Save the extracted text in the form of a json file.

    Args:
        dataset (Dataset): Audio dataset Class
        output_path (str): Output path
        model_size (str): Size of the whisper model.
        language (str): Language of the audio file to run STT.

    Returns:
        Dict: Dictionary of the text values of audio files in the dataset.

    """
    audios = dataset.audios
    stt_dict = {}

    bar = tqdm(audios,
               total=len(audios),
               leave=True,
               )

    for audio in bar:
        text = whisper_stt(audio, model_size, language)
        stt_dict[audio.name] = text

    with open(Path(output_path) / Path(f'{dataset.dataset_name}.json'), 'w') as f:
        json.dump(stt_dict, f, indent=4)

    return stt_dict
