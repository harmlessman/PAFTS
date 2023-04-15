
from pydub import AudioSegment
from pathlib import Path

AUDIO_FILE_EXT = [
    'wav',
    'mp3',
    'raw',
    'pcm',
    'mp4',
    'mkv'
]


def is_audio(path):
    file = Path(path)
    if file.suffix[1:] in AUDIO_FILE_EXT:
        return True
    return False


def get_duration(path):
    audio = AudioSegment.from_file(path)
    return audio.duration_seconds


def get_total_duration(path):
    total_duration = 0
    file_list = get_audio_file(path)

    for file in file_list:
        total_duration += get_duration(file)
    return total_duration


def get_audio_file(path):
    return [p for p in Path(path).glob("**/*") if is_audio(p)]


def get_file_num(path):
    return len(get_audio_file(path))

