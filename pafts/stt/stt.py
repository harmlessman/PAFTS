import json
from pathlib import Path
from collections import defaultdict

import whisper
from whisper.tokenizer import LANGUAGES
from tqdm import tqdm

from pafts.datasets.dataset import Dataset

whisper_model = {key: None for key in whisper._MODELS}


def whisper_stt(
        audio: Path,
        model_size='base',
        language=None,
):
    """
        Use the Whipser[https://github.com/openai/whisper] STT model to extract text.
        If there is no gpu or low performance, use the base model.

        Args:
            audio (Data): Audio data.
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

    result = whisper_model[model_size].transcribe(str(audio))

    return result['text']


def STT(
        dataset: Dataset,
        output_format='json',
        model_size='base',
        language=None
):
    """
    Read the audio files in the dataset, and use the stt function to extract text.
    Save the extracted text in the form of a json file.

    Args:
        dataset (Dataset): Audio dataset Class
        output_format (str): Output format, Defaults is json (json or txt)
        model_size (str): Size of the whisper model.
        language (str): Language of the audio file to run STT.

    Returns:
        Dict: Dictionary of the text values of audio files in the dataset.

    """
    audios = dataset.audios
    stt_dict = defaultdict(dict)

    output_path = dataset.output_path

    bar = tqdm(audios,
               total=len(audios),
               leave=True,
               )

    for audio in bar:
        text = whisper_stt(audio, model_size, language)
        stt_dict[audio.parent.name][audio.name] = text

    for speaker in stt_dict:
        if output_format == 'json':
            with open(Path(output_path) / Path(f'{speaker}.json'), 'w', encoding='UTF8') as f:
                json.dump(stt_dict[speaker], f, indent=4, ensure_ascii=False)
        elif output_format == 'txt':
            with open(Path(output_path) / Path(f'{speaker}.txt'), 'w', encoding='UTF8') as f:
                for k, v in stt_dict[speaker]:
                    f.write(f'{k}|{v}\n')
        else:
            raise ValueError(
                f"[!] Please choose one of the following format: json, txt.")

    return stt_dict
