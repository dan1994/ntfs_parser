from ntfs.utils.volume_info import VolumeInfo
from ntfs.mft.file_entry import FileEntry


class File:

    def __init__(self, volume_info: VolumeInfo, file_entry: FileEntry):
        self._volume_info = volume_info
        self._file_entry = file_entry

        self._volume_file = volume_info.get_volume_file()

    def __enter__(self) -> 'File':
        self.open()
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def open(self) -> None:
        self._volume_file.open()

    def close(self) -> None:
        self._volume_file.close()

    def read(self) -> bytes:
        return self._file_entry.data()
