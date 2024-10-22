from pafts.datasets.dataset import Dataset

from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pydub import AudioSegment
from pyannote.audio import Pipeline
import torch


def diarization(
    dataset: Dataset,
        hf_token,


):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token)

    pipeline.to(torch.device("cuda"))
    seg = None
    padding = AudioSegment.silent(duration=1000)

    for audio in dataset.audios:
        print(audio.name)
        if not seg:
            seg = AudioSegment.from_file(audio)
        else:
            seg += AudioSegment.from_file(audio)
        seg += padding

    samples = seg.get_array_of_samples()
    sample_rate = seg.frame_rate

    waveform = torch.tensor(samples).float().reshape(1, -1)

    audio_input = {
        "waveform": waveform,
        "sample_rate": sample_rate
    }

    diarization_audio = pipeline('audio_20min/obama.mp3')
    print(diarization_audio)

    for i, (turn, _, speaker) in enumerate(diarization_audio.itertracks(yield_label=True)):
        start_ms = turn.start * 1000
        end_ms = turn.end * 1000

        speaker_folder = dataset.output_path / f"speaker_{speaker}"
        speaker_folder.mkdir(parents=True, exist_ok=True)

        segment = seg[start_ms:end_ms]

        output_file_path = speaker_folder / f"{i}_segment.wav"
        segment.export(output_file_path, format="wav")

        print(f"Saved segment {i} for speaker {speaker}: {output_file_path}")


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

