from typing import Tuple

from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.mft.data_run import DataRunHeader
from ntfs.utils.header import HeaderList
from ntfs.utils import ntfs_logger


class DataRuns(HeaderList):

    HEADER_TYPE = DataRunHeader

    def data(self):
        data = b''
        with LogicalVolumeFile(self._volume_info.volume_letter) as volume_file:
            for offset, length in self:
                ntfs_logger.debug(f'Retrieving run at {hex(offset)} with '
                                  f'{length}')
                volume_file.seek(offset)
                data += volume_file.read(length)
        return data

    def __iter__(self) -> 'DataRuns':
        self._absolute_offset = 0
        self._index = 0
        return self

    def __next__(self) -> Tuple[int, int]:
        if not self._headers[self._index].is_valid:
            raise StopIteration()

        self._absolute_offset += self._headers[self._index].offset
        length = self._headers[self._index].length

        self._index += 1

        return self._absolute_offset, length
