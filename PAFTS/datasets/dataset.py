from pathlib import Path

from pydub import AudioSegment

AUDIO_FILE_EXT = [
    '.wav',
    '.mp3',
    '.raw',
    '.pcm',
    '.mp4',
    '.mkv'
]


def is_audio(path):
    file = Path(path)
    if file.suffix in AUDIO_FILE_EXT:
        return True
    return False


def get_duration(path):
    audio = AudioSegment.from_file(path)
    return audio.duration_seconds


class Dataset:
    def __init__(
            self,
            path: str = "",
            dataset_name: str = "",
            output_path: str = "",
            language: str = "",

    ):
        self.path = Path(path)

        if dataset_name:
            self.dataset_name = dataset_name
        else:
            self.dataset_name = Path(path).name

        if output_path:
            self.output_path = output_path
        else:
            self.output_path = Path(path).joinpath('output')

        self.language = language

        self.items = self.get_audio_file()

    def get_total_duration(self):
        total_duration = 0
        file_list = [p for p in self.path.glob("**/*") if is_audio(p)]

        for file in file_list:
            total_duration += get_duration(file)
        return total_duration

    def get_audio_file(self):
        return [p for p in self.path.glob("**/*") if is_audio(p)]

    def get_file_num(self):
        total_num = 0
        for p in self.path.glob('**/*'):
            if is_audio(p):
                total_num += 1
        return total_num

    def update_item(self):
        self.items = self.get_audio_file()
        return self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


if __name__ == '__main__':
    d = Dataset('C:\\Users\\82109\\Desktop\\PAFTS\\data')
    print(d.get_total_duration())
    print(len(d))
    print(d.path)
    print(d.dataset_name)
    print(d.output_path)
    print(d.language)
    print(d.get_file_num())
    print(d.get_audio_file())
    print(d.update_item())
    print(d.items)