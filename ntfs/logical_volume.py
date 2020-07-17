from os.path import split

from ntfs.utils import ntfs_logger
from ntfs.mft.mft import Mft
from ntfs.file import File
from ntfs.vbr import Vbr


class LogicalVolume:

    def __init__(self, volume_letter: str):
        vbr: Vbr = Vbr(volume_letter)
        self._mft: Mft = Mft(volume_letter, vbr.get_mft_start_address())

    def get_file(self, path: str) -> File:
        ntfs_logger.info(f'Searching for {path}...')

        actual_path = LogicalVolume._get_actual_path(path)

        for file_entry in self._mft:
            file_path = file_entry.path
            ntfs_logger.info(f'File name: {file_path}')
            if file_path == actual_path:
                ntfs_logger.info('Found!')
                return File(file_entry)

        raise RuntimeError('File doesn\'t exist')

    @staticmethod
    def _get_actual_path(path):
        path_parts = split(path)
        if len(path_parts) == 2 and path_parts[1][0] == '$':
            return path_parts[1]
        return path
