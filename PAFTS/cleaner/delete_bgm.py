from spleeter.separator import Separator
from spleeter.utils.logging import logger
from tqdm import tqdm

from pathlib import Path
from filecmp import cmp
from multiprocessing import freeze_support
import logging

from PAFTS.datasets.dataset import Dataset
from PAFTS.utils.data_info import get_audio_file

logger.setLevel(logging.WARNING)


def delete_bgm(dataset: Dataset):
    freeze_support()

    print(f'Delete_bgm is starting...\n')

    output_path = dataset.output_path

    items = dataset.get_audio_file()
    output_path_items = get_audio_file(output_path)

    if not output_path.exists():
        output_path.mkdir()

    if any(Path(output_path).iterdir()):
        print(f'{output_path} is not empty!')
        print(f'If output_path has an item, pass it.\n')

    items = [item for item in items if item not in output_path_items]

    separator = Separator('spleeter:2stems')
    accompaniment = Path('accompaniment.wav')
    vocal = Path('vocals.wav')

    bar = tqdm(items,
               total=len(items),
               desc='spleeter_progress',
               leave=True,
               )

    for item in bar:
        bar.set_description(item.name)
        separator.separate_to_file(
            str(item),
            str(output_path),
            filename_format='{instrument}.{codec}'
        )

        name = Path(item.name)

        Path(output_path / accompaniment).unlink()

        if (output_path / name).exists():
            if cmp((output_path / name), (output_path / vocal)):
                (output_path / vocal).unlink()

            else:
                i = 0
                while (output_path / Path(f'{item.stem}_{i}{item.suffix}')).exists():
                    i += 1
                (output_path / vocal).rename(output_path / Path(f'{item.stem}_{i}{item.suffix}'))

        else:
            (output_path / vocal).rename(output_path / name)

    print('Done!')
