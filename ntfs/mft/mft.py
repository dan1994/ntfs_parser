from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.mft.file_entry import FileEntry
from ntfs.utils import ntfs_logger
from ntfs.file import File


class Mft:

    def __init__(self, volume_letter: str, base_address: int,
                 cluster_size_in_bytes: int):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        with LogicalVolumeFile(volume_letter) as volume_file:
            volume_file.seek(base_address)
            mft_entry_content = volume_file.read(FileEntry.SIZE)

        mft_entry = FileEntry(mft_entry_content, 0)
        with File(volume_letter, cluster_size_in_bytes, mft_entry) as mft_file:
            self._data = mft_file.read()

        self._base_address = base_address

    def __iter__(self) -> 'Mft':
        self._entry_base_address = 0
        return self

    def __next__(self) -> FileEntry:
        while self._entry_base_address < len(self._data):
            ntfs_logger.\
                info(f'Retrieving file entry at '
                     f'{hex(self._base_address + self._entry_base_address)}')

            entry = FileEntry(
                self._data[self._entry_base_address:
                           self._entry_base_address + FileEntry.SIZE], 0)
            self._entry_base_address += FileEntry.SIZE

            if entry.is_valid:
                return entry
            else:
                ntfs_logger.warning('Invalid file entry, skipping...')

        raise StopIteration()
