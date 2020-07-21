from ntfs.utils.volume_info import VolumeInfo
from ntfs.mft.file_entry import FileEntry
from ntfs.utils import ntfs_logger
from ntfs.file import File


class Mft:

    def __init__(self, volume_info: VolumeInfo, base_address: int):
        ntfs_logger.debug(f"{self.__class__}")

        self._volume_info = volume_info
        self._base_address = base_address

        self._read_mft_data()

    def __iter__(self) -> 'Mft':
        self._entry_base_address = 0
        return self

    def __next__(self) -> FileEntry:
        while self._entry_base_address < len(self._data):
            ntfs_logger.\
                info(f'Retrieving file entry at '
                     f'{hex(self._base_address + self._entry_base_address)}')

            entry = FileEntry(self._volume_info,
                              self._data[self._entry_base_address:
                                         self._entry_base_address +
                                         FileEntry.SIZE])
            self._entry_base_address += FileEntry.SIZE

            if entry.is_valid:
                return entry
            else:
                ntfs_logger.warning('Invalid file entry, skipping...')

        raise StopIteration()

    def _read_mft_data(self) -> None:
        with self._volume_info.get_volume_file() as volume_file:
            volume_file.seek(self._base_address)
            mft_entry_content = volume_file.read(FileEntry.SIZE)

        mft_entry = FileEntry(self._volume_info, mft_entry_content)
        with File(self._volume_info, mft_entry) as mft_file:
            self._data = mft_file.read()
