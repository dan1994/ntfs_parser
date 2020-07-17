from ntfs.mft.file_entry import FileEntry
from ntfs.utils import ntfs_logger


class Mft:

    def __init__(self, volume_letter: str, base_address: int):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        self._volume_letter: str = volume_letter
        self._base_address: int = base_address

        self._get_mft_size()

    def __iter__(self) -> 'Mft':
        self._entry_base_address: int = self._base_address
        return self

    def __next__(self) -> FileEntry:
        entry = None
        while not entry and not self._reached_end_of_mft():
            entry = FileEntry(self._volume_letter, self._entry_base_address)
            self._entry_base_address += FileEntry.SIZE

        if self._reached_end_of_mft():
            raise StopIteration()

        return entry

    def _get_mft_size(self):
        mft_file_entry: FileEntry = \
            FileEntry(self._volume_letter, self._base_address)
        self._size: int = mft_file_entry.file_size

    def _reached_end_of_mft(self):
        return self._entry_base_address == self._base_address + self._size
