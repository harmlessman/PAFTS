from pydub import AudioSegment

from pafts.datasets.dataset import Dataset
from pafts.utils.data_info import AUDIO_FILE_EXT


def change_sr(dataset: Dataset, sr: int = 22050):
    """Change sampling rate of the audio files"""
    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio = audio.set_frame_rate(sr)
        audio.export(item, format=item.suffix[1:])


def change_channel(dataset: Dataset, channel: int = 1):
    """Change channel of the audio files"""
    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio = audio.set_channels(channel)
        audio.export(item, format=item.suffix[1:])


def change_format(dataset: Dataset, formats: str = 'wav'):
    """Change format of the audio files"""
    if formats not in AUDIO_FILE_EXT:
        raise Exception(f'Do not support {formats} format.')

    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio.export(item, format=formats)




