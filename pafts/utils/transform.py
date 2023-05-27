import sys

from pydub import AudioSegment
from tqdm import tqdm

from pafts.datasets.dataset import Dataset
from pafts.utils import AUDIO_FORMATS


def change_sr(dataset: Dataset, sr: int = 22050):
    """Change sampling rate of the audio files"""
    items = dataset.get_audio_file()

    bar = tqdm(items,
               total=len(items),
               desc='change_sr',
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        audio = AudioSegment.from_file(item)
        audio = audio.set_frame_rate(sr)
        audio.export(item, format=item.suffix[1:])


def change_channel(dataset: Dataset, channel: int = 1):
    """Change channel of the audio files"""
    items = dataset.get_audio_file()

    bar = tqdm(items,
               total=len(items),
               desc='change_channel',
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        audio = AudioSegment.from_file(item)
        audio = audio.set_channels(channel)
        audio.export(item, format=item.suffix[1:])


def change_format(dataset: Dataset, formats: str = 'wav'):
    """Change format of the audio files"""
    if formats not in AUDIO_FORMATS:
        raise Exception(f'Do not support {formats} format.')

    items = dataset.get_audio_file()

    bar = tqdm(items,
               total=len(items),
               desc='change_format',
               leave=True,
               file=sys.stdout,
               )

    for item in bar:
        audio = AudioSegment.from_file(item)
        item.unlink()
        audio.export(item.with_suffix('.' + formats), format=formats)
