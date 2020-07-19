from typing import Generator, Tuple, Type
from struct import error as struct_error
from struct import unpack_from

from ntfs.utils import ntfs_logger

HeaderGenerator = Generator[Tuple[type, int], None, None]


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

        self._data = unpack_from('=' + self.FMT, data, offset)

    def is_valid(self) -> bool:
        return False

    def __len__(self) -> int:
        return self.FMT.count('B') + 2 * self.FMT.count('H') + \
            4 * self.FMT.count('I') + 8 * self.FMT.count('Q')


class HeaderList(MultiHeader):

    HEADER_TYPE = None

    def __init__(self, data: bytes, offset: int):
        try:
            super(HeaderList, self).__init__(data, offset)
        except struct_error:
            ntfs_logger.warning(
                'Reached end of data while parsing headers')

    def __iter__(self) -> 'HeaderList':
        self._index = 0
        return self

    def __next__(self) -> Type[Header]:
        if self._index >= len(self):
            raise StopIteration()

        header = self._headers[self._index]
        self._index += 1
        return header

    def __getitem__(self, index: int) -> Type[Header]:
        return self._headers[index]

    def __len__(self) -> int:
        return len(self._headers)

    def _get_next_header_info(self) -> HeaderGenerator:
        current_offset = 0
        yield self.HEADER_TYPE, current_offset

        while self._headers[-1].is_valid:
            current_offset += len(self._headers[-1])
            yield self.HEADER_TYPE, current_offset
