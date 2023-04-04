from spleeter.separator import Separator
from spleeter.utils.logging import logger
from tqdm import tqdm


from pathlib import Path
from multiprocessing import freeze_support
import logging

from PAFTS.datasets.dataset import Dataset

logger.setLevel(logging.WARNING)
logging.getLogger('tensorflow').setLevel(logging.CRITICAL)


def delete_bgm(dataset: Dataset):
    """
    Remove BGM from the audio file and save audio file as a same file name.
    Please note that the original file will be deleted.

    Spleeter library was used to remove the BGM

    Args:
        dataset (Dataset): Dataset.
    """

    freeze_support()

    print(f'> Delete BGM...')
    print(f'| > Number of items : {dataset.get_file_num()}')
    print(f'| > Path : {dataset.path}\n')

    items = dataset.get_audio_file()

    separator = Separator('spleeter:2stems')
    accompaniment = Path('accompaniment.wav')
    vocal = Path('vocals.wav')

    bar = tqdm(items,
               total=len(items),
               desc='spleeter_progress',
               leave=True,
               )

    success = 0
    failure = []

    for item in bar:
        bar.set_description(item.name)
        try:
            separator.separate_to_file(
                str(item),
                str(dataset.path),
                filename_format='{instrument}.{codec}'
            )
            success += 1

        except:
            failure.append(item)
            continue

        name = Path(item.name)

        (dataset.path / accompaniment).unlink()
        (dataset.path / name).unlink()

        (dataset.path / vocal).rename(dataset.path / name)

    print(f'\n| > Number of Success items : {success}')
    print(f'| > Number of failure items : {len(failure)}')
    print(f'| > fail item')
    for f in failure:
        print(f'    > {f}')

