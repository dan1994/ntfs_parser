from ntfs.utils.volume_info import VolumeInfo
from ntfs.mft.file_entry import FileEntry


class File:

    def __init__(self, volume_info: VolumeInfo, file_entry: FileEntry):
        self._volume_info = volume_info
        self._file_entry = file_entry

    def __enter__(self) -> 'File':
        self.open()
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass

    def read(self) -> bytes:
        return self._file_entry.data()
