from os.path import basename

from ntfs.utils.volume_info import VolumeInfo
from ntfs.utils import ntfs_logger
from ntfs.mft.mft import Mft
from ntfs.file import File
from ntfs.vbr import Vbr


class LogicalVolume:

    def __init__(self, volume_letter: str):
        vbr = Vbr.read_vbr(volume_letter)
        self._volume_info = VolumeInfo(volume_letter,
                                       vbr.sector_size_in_bytes,
                                       vbr.cluster_size_in_sectors)

        mft_start_address = vbr.mft_logical_cluster_number * \
            self._volume_info.cluster_size_in_bytes

        ntfs_logger.info(f'MFT is at {hex(mft_start_address)}')

        self._mft = Mft(self._volume_info, mft_start_address)

    def get_file(self, path: str) -> File:
        ntfs_logger.info(f'Searching for {path}...')

        name = basename(path)

        for file_entry in self._mft:
            ntfs_logger.info(f'File name: {file_entry.name}')

            if file_entry.name == name:
                ntfs_logger.info('Found!')
                return File(self._volume_info, file_entry)

        raise RuntimeError('File doesn\'t exist')
