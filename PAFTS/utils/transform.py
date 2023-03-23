from pydub import AudioSegment
from pathlib import Path
from data_info import is_audio


def change_sr(path, sr=22050):
    file_list = [p for p in Path(path).glob("**/*") if is_audio(p)]

    for file in file_list:
        audio = AudioSegment.from_file(file)
        audio = audio.set_frame_rate(sr)
        audio.export(file, format=file.suffix[1:])


def change_channel(path, channel=1):
    file_list = [p for p in Path(path).glob("**/*") if is_audio(p)]

    for file in file_list:
        audio = AudioSegment.from_file(file)
        audio = audio.set_channels(channel)
        audio.export(file, format=file.suffix[1:])
