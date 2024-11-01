import shutil
from pathlib import Path
import uuid
from datetime import datetime

from pafts.datasets.dataset import Dataset
from pafts.diarization.diarization import diarization
from pafts.separator.separator import separator
from pafts.stt.stt import STT


class PAFTS:
    """
        Make audio files into a dataset for TTS.

        Args:
        path (str): Directory path with audio files.
        dataset_name (str, optional): Dataset name. Defaults to dataset_path's directory name.
        language (str, optional): Language using BCP 47 language tag. Defaults to 'en-us' (English)
        output_path (str): Output Directory. Defaults to './pafts_output'

        Example with quick start:
        p = PAFTS(
            path = 'your_audio_directory_path',
            output_path = 'output_path',
            hf_token="HUGGINGFACE_ACCESS_TOKEN_GOES_HERE"
        )
        p.run()


        """

    def __init__(
            self,
            path: str = None,
            dataset_name: str = None,
            language: str = None,
            output_path: str = 'pafts_output',
            hf_token: str = None
    ):

        self._hf_token = hf_token

        self._dataset = Dataset(
            path=path,
            dataset_name=dataset_name,
            language=language,
            output_path=output_path
        )

    def separator(self):
        separator(self._dataset)
        return

    def diarization(self):
        if not self._hf_token:
            raise TypeError("[!] Hugging Face access token is required to use diarization model.")

        diarization(self._dataset, self._hf_token)

        return

    def stt(self, output_format='json', model_size='large'):
        STT(self._dataset, output_format=output_format, model_size=model_size)
        return

    def _stage_process(self, process_function, *args, **kwargs):
        # Create unique temp directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex
        temp_dir = Path.cwd() / f"temp_dir_{timestamp}_{unique_id}"
        temp_dir.mkdir(exist_ok=True)

        self._dataset.output_path = temp_dir
        process_function(self._dataset, *args, **kwargs)

        # Update dataset path
        self._dataset.path = temp_dir

        return temp_dir

    def run(self):
        original_output = self._dataset.output_path

        # Stage 1: separator
        temp_dir1 = self._stage_process(separator)

        # Stage 2: diarization
        temp_dir2 = self._stage_process(diarization, hf_token=self._hf_token)

        # Stage 3: STT
        temp_dir3 = self._stage_process(STT)

        original_output.mkdir(exist_ok=True)

        for temp_dir in [temp_dir2, temp_dir3]:
            for file in temp_dir.rglob('*'):
                if file.is_file():
                    relative_path = file.relative_to(temp_dir)
                    destination = original_output / relative_path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(file, destination)

        # Cleanup
        for temp_dir in [temp_dir1, temp_dir2, temp_dir3]:
            shutil.rmtree(temp_dir, ignore_errors=True)
