from pydub import AudioSegment
from PAFTS.datasets.dataset import Dataset
from PAFTS.datasets.dataset import AUDIO_FILE_EXT


def change_sr(dataset: Dataset, sr: int = 22050):
    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio = audio.set_frame_rate(sr)
        audio.export(item, format=item.suffix[1:])


def change_channel(dataset: Dataset, channel: int = 1):
    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio = audio.set_channels(channel)
        audio.export(item, format=item.suffix[1:])


def change_format(dataset: Dataset, formats: str = 'wav'):
    if formats not in AUDIO_FILE_EXT:
        return

    items = dataset.get_audio_file()

    for item in items:
        audio = AudioSegment.from_file(item)
        audio.export(item, formats=formats)


