from os.path import basename

from ntfs.utils import ntfs_logger
from ntfs.mft.mft import Mft
from ntfs.file import File
from ntfs.vbr import Vbr


class LogicalVolume:

    def __init__(self, volume_letter: str):
        vbr = Vbr(volume_letter)

        mft_start_address = vbr.get_mft_start_address()
        ntfs_logger.info(f'MFT is at {hex(mft_start_address)}')
        self._mft = Mft(volume_letter, mft_start_address)

    def get_file(self, path: str) -> File:
        ntfs_logger.info(f'Searching for {path}...')

        actual_path = basename(path)

        for file_entry in self._mft:
            file_path = file_entry.path
            ntfs_logger.info(f'File name: {file_path}')

            if file_path == actual_path:
                ntfs_logger.info('Found!')
                return File(file_entry)

        raise RuntimeError('File doesn\'t exist')
