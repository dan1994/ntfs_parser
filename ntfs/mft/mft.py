from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.mft.file_entry import FileEntry
from ntfs.utils import ntfs_logger


class Mft:

    def __init__(self, volume_letter: str, base_address: int):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        self._volume_file = LogicalVolumeFile(volume_letter)
        self._base_address = base_address

        self._find_mft_size()

    def __del__(self) -> None:
        self._volume_file.close()

    def __iter__(self) -> 'Mft':
        self._volume_file.open()
        self._volume_file.seek(self._base_address)
        self._entry_base_address = self._base_address
        return self

    def __next__(self) -> FileEntry:
        entry = None
        while not entry and not self._reached_end_of_mft():
            ntfs_logger.info(
                f'Retrieving file entry at {hex(self._entry_base_address)}')

            entry_content = self._volume_file.read(FileEntry.SIZE)
            entry = FileEntry(entry_content, 0)
            self._entry_base_address += FileEntry.SIZE

        if self._reached_end_of_mft():
            self._volume_file.close()
            raise StopIteration()

        return entry

    def _find_mft_size(self) -> None:
        mft_size = self._get_mft_entry().file_size
        assert mft_size % FileEntry.SIZE == 0, \
            'MFT size should be a multiple of file entry size'
        self._size = mft_size

    def _get_mft_entry(self) -> FileEntry:
        self._volume_file.open()
        self._volume_file.seek(self._base_address)
        mft_entry_content = self._volume_file.read(FileEntry.SIZE)
        self._volume_file.close()
        return FileEntry(mft_entry_content, 0)

    def _reached_end_of_mft(self) -> bool:
        return self._entry_base_address == self._base_address + self._size
