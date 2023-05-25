from pathlib import Path
import json

from pydub import AudioSegment
from tqdm import tqdm


def rmtree(path):
    """
    This function acts like shutil.rmtree.
    Delete all directories and files in the path.

    """
    for d in Path(path).glob('*'):
        if d.is_dir():
            rmtree(d)
        else:
            d.unlink()
    path.rmdir()


def save_dict(path, dic: dict, file_name: str = 'text.json'):
    """
    Save the dict as a json file.

    Args:
        path (str or Path): Path to save the text file.
        dic (dict): Audio file and text pairs.
        file_name (str, optional): Output text file name. Defaults to 'text.json'.

    """
    with open(Path(path) / Path(file_name), 'w', encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False, indent='\t')

    print(f'Saved at {Path(path) / Path(file_name)}')
    return Path(path) / Path(file_name)


def delete_none_value(path, dic: dict):
    """
    This function deletes an element with a value of None in dic,
    and deletes the audio file corresponding to the key.

    Example:
        before => {'1_001.wav' : "Hello", '1_002.wav' : None, '1_003.wav' : "This is an apple"}
        after => {'1_001.wav' : "Hello.", '1_003.wav' : "This is an apple."}

    Args:
        path (str or Path): dataset's path
        dic (dict): Audio file and text pairs

    Return:
        Dict: Audio file and text pairs with no value None

    """
    del_list = []

    for key in list(dic):
        if dic[key] is None:
            del_list.append(key)

    for key in del_list:
        dic.pop(key)
        (Path(path) / Path(key)).unlink()

    print(f'| > Numbers of deleted files : {len(del_list)}')

    if del_list:
        print(f'| > Deleted files')
        for f in del_list:
            print(f'    > {f}')

    return dic


def make_key_file(path: str = '', file_name: str = 'key.json'):
    """
    Make key file frame as a json file.
    You can leave unused API keys blank.

    Args:
        path (str): key file path.
        file_name (str): key file name.
    """

    key_frame = {
        'google_cloud_stt': '',
        'azure_stt': {
            'key': '',
            'location': ''
        }
    }
    with open(Path(path) / Path(file_name), 'w', encoding="utf-8") as f:
        json.dump(key_frame, f, ensure_ascii=False, indent='\t')


def audio_duration_filter(audio_files: list, min_dur: float = 0, max_dur: float = float('inf'), path: str = ''):
    """
    Delete audio files that are out of time range.

    Args:
        audio_files (list): Audio file name list. if elements
        min_dur (float): Minimum audio file duration.
        max_dur (float): Maximum audio file duration.
        path (str): Audio file path.
    """

    if min_dur > max_dur:
        print(f'Min, Max range is wrong!')
        return

    deleted_count = 0

    bar = tqdm(audio_files,
               total=len(audio_files),
               desc='dur_filter',
               leave=True,
               )

    for audio_file in bar:
        audio = AudioSegment.from_file(Path(path) / Path(audio_file))
        audio_dur = audio.duration_seconds

        if audio_dur < min_dur or audio_dur > max_dur:
            audio_file.unlink()
            deleted_count += 1

    print(f'Minimum duration = {min_dur} seconds')
    print(f'Maximum duration = {max_dur} seconds')
    print(f'Deleted file num : {deleted_count}')
