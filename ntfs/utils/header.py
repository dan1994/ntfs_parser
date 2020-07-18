from typing import Generator, Tuple
from struct import unpack_from

from ntfs.utils import ntfs_logger

HeaderGenerator = Generator[Tuple(type, int), None, None]


class MultiHeader:

    def __init__(self, data: bytes, offset: int):
        ntfs_logger.debug(f'{self.__class__}, {hex(offset)}')

        self._data = data
        self._offset = offset
        self._headers = []

        self._parse_headers()

    def _parse_headers(self) -> None:
        for header_type, offset in self._get_next_header_info():
            total_offset = self._offset + offset
            self._headers.append(header_type(self._data, total_offset))

    def _get_next_header_info(self) -> HeaderGenerator:
        pass


class Header:

    FMT = ''

    def __init__(self, data: bytes, offset: int):
        ntfs_logger.debug(f'{self.__class__}, {hex(offset)}')

        self._data = unpack_from(self.FMT, data, offset)

    def __len__(self) -> int:
        return self.FMT.count('B') + 2 * self.FMT.count('H') + \
            4 * self.FMT.count('I') + 8 * self.FMT.count('Q')
