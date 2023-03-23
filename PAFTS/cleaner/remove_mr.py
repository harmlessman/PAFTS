from spleeter.separator import Separator
from pathlib import Path
from PAFTS.utils.data_info import is_audio
from multiprocessing import freeze_support


def m(path):
    file_list = [p for p in Path(path).glob("**/*") if is_audio(p)]
    separator = Separator('spleeter:2stems')
    for file in file_list:
        separator.separate_to_file(str(file), 'C:\\Users\\82109\\Desktop\\PAFTS\\data\\out')
        print(file)

    print('done')


if __name__ == '__main__':
    freeze_support()
    m('C:\\Users\\82109\\Desktop\\PAFTS\\data')
