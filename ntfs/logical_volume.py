from os.path import basename

from ntfs.utils import ntfs_logger
from ntfs.mft.mft import Mft
from ntfs.file import File
from ntfs.vbr import Vbr


class LogicalVolume:

    def __init__(self, volume_letter: str):
        self._volume_letter = volume_letter

        self._vbr = Vbr(volume_letter)
        self._cluster_size_in_bytes = self._vbr.cluster_size_in_sectors * \
            self._vbr.sector_size_in_bytes
        mft_start_address = self._vbr.mft_index * self._cluster_size_in_bytes

        ntfs_logger.info(f'MFT is at {hex(mft_start_address)}')
        self._mft = Mft(volume_letter, mft_start_address,
                        self._cluster_size_in_bytes)

    def get_file(self, path: str) -> File:
        ntfs_logger.info(f'Searching for {path}...')

        name = basename(path)

        for file_entry in self._mft:
            ntfs_logger.info(f'File name: {file_entry.name}')

            if file_entry.name == name:
                ntfs_logger.info('Found!')
                return File(self._volume_letter,
                            self._cluster_size_in_bytes, file_entry)

        raise RuntimeError('File doesn\'t exist')
