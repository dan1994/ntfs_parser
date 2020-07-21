from struct import error as struct_error
from struct import unpack
from typing import Type

from ntfs.utils.volume_info import VolumeInfo
from ntfs.utils import ntfs_logger


class Header:

    FMT = ''

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        ntfs_logger.debug(f'{self.__class__}')

        data_to_unpack = data[:self._fmt_size_in_bytes()]

        self._data = unpack('=' + self.FMT, data_to_unpack)

    def is_valid(self) -> bool:
        return False

    def __len__(self) -> int:
        return self._fmt_size_in_bytes()

    def _fmt_size_in_bytes(self) -> int:
        return self.FMT.count('B') + 2 * self.FMT.count('H') + \
            4 * self.FMT.count('I') + 8 * self.FMT.count('Q')


class HeaderList:

    HEADER_TYPE = None

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        ntfs_logger.debug(f'{self.__class__}')

        self._volume_info = volume_info

        try:
            self._collect_headers(data)
        except struct_error:
            ntfs_logger.warning('Data ran out while parsing header list')

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

    def _collect_headers(self, data) -> None:
        self._headers = []
        self._headers.append(self.HEADER_TYPE(self._volume_info, data))

        while self._headers[-1].is_valid:
            data = data[len(self._headers[-1]):]
            self._headers.append(self.HEADER_TYPE(self._volume_info, data))
