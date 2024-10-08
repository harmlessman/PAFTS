from pafts.datasets.dataset import Dataset

from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pydub import AudioSegment


def vad(
        dataset: Dataset,
        min_silence_duration_ms=500,
        padding_duration_ms=200,

):
    model = load_silero_vad()
    audios = dataset.audios
    stamp = []
    new_audios = []

    for audio in audios:
        wav = read_audio(str(audio))

        speech_timestamps = get_speech_timestamps(wav, model, min_silence_duration_ms=min_silence_duration_ms)

        for speech_timestamp in speech_timestamps:
            start = speech_timestamp['start']
            end = speech_timestamp['end']
            start /= 16000
            end /= 16000
            stamp.append((start, end))

        audio_segment = AudioSegment.from_file(audio)

        for i, (start, end) in enumerate(stamp):
            start_ms = start * 1000
            end_ms = end * 1000

            segment = audio_segment[start_ms:end_ms]
            padding = AudioSegment.silent(duration=padding_duration_ms)
            segment = padding + segment + padding

            file_name = audio.with_name(f'{audio.stem}_{i}{audio.suffix}')
            file_name = file_name.name

            path = (dataset.output_path / file_name).resolve()
            segment.export(path, format=audio.suffix[1:])

            new_audios.append(path)

    dataset.audios = new_audios

    return new_audios