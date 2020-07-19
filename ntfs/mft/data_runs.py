from typing import Tuple

from ntfs.mft.data_run import DataRunHeader
from ntfs.utils.header import HeaderList


class DataRuns(HeaderList):

    HEADER_TYPE = DataRunHeader

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
