import uuid
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from pafts.datasets.dataset import Dataset

from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pydub import AudioSegment
from pyannote.audio import Pipeline
import torch


def generate_unique_filename(format="wav"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex
    return f"temp_audio_{timestamp}_{unique_id}.{format}"


def diarization(
        dataset: Dataset,
        hf_token,

):
    """
    This function performs diarization (speaker separation) on the audio files,
    splits them by sentence, and then separates the audio by each speaker.

    Args:
        dataset (Dataset): Dataset instance.
        hf_token (str): Huggingface access token.

    Return:
        new_audios (list): List of new audio path.

    """

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token)

    # check using gpu or not
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using GPU...")
    else:
        device = torch.device("cpu")
        print("Using CPU...")

    pipeline.to(device)

    seg = None
    padding = AudioSegment.silent(duration=1000)

    for audio in dataset.audios:
        if not seg:
            seg = AudioSegment.from_file(audio)
        else:
            seg += AudioSegment.from_file(audio)
        seg += padding

    temp_file_path = dataset.output_path / generate_unique_filename()

    # create audio temp file
    seg.export(temp_file_path, format='wav')

    # diarization
    diarization_audio = pipeline(f"{temp_file_path}")

    speaker_num_list = defaultdict(int)
    new_audios = []

    for i, (turn, _, speaker) in enumerate(diarization_audio.itertracks(yield_label=True)):
        start_ms = turn.start * 1000
        end_ms = turn.end * 1000

        speaker_folder = dataset.output_path / f"speaker_{speaker}"
        speaker_folder.mkdir(parents=True, exist_ok=True)

        segment = seg[start_ms:end_ms]

        output_file_path = speaker_folder / f"{speaker}_{speaker_num_list[speaker]}.wav"
        segment.export(output_file_path, format="wav")

        speaker_num_list[speaker] += 1  # +1

        new_audios.append(speaker_folder / f"{speaker}_{speaker_num_list[speaker]}.wav")

    # delete temp file
    if Path(temp_file_path).exists():
        temp_file_path.unlink()

    dataset.audios = new_audios

    return new_audios


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
