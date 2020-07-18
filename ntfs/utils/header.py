from struct import unpack_from

from ntfs.utils import ntfs_logger


class MultiHeader:

    def __init__(self, data, offset):
        ntfs_logger.debug(f'{self.__class__}, {hex(offset)}')

        self._data = data
        self._offset = offset
        self._headers = []

        self._parse_headers()

    def _parse_headers(self):
        for header_type, offset in self._get_next_header_info():
            total_offset = self._offset + offset
            self._headers.append(header_type(self._data, total_offset))

    def _get_next_header_info(self):
        pass


class Header:

    FMT = ''

    def __init__(self, data, offset):
        ntfs_logger.debug(f'{self.__class__}, {hex(offset)}')

        self._data = unpack_from(self.FMT, data, offset)

    def __len__(self):
        return self.FMT.count('B') + 2 * self.FMT.count('H') + \
            4 * self.FMT.count('I') + 8 * self.FMT.count('Q')
