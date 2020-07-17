from struct import unpack

from ntfs.utils.logical_volume_file import LogicalVolumeFile


class MultiHeader:

    def __init__(self, volume_letter, base_address):
        self._volume_letter = volume_letter
        self._base_address = base_address
        self._headers = []

        self._parse_headers()

    def _parse_headers(self):
        for header_type, offset in self._get_next_header_info():
            self._headers.append(header_type(self._volume_letter, offset))

    def _get_next_header_info(self):
        pass


class Header:

    def __init__(self, volume_letter, base_address, fmt=''):
        self._volume_letter = volume_letter
        self._base_address = base_address
        self._fmt = fmt
        self._size = Header._get_size_from_fmt(self._fmt)

        self._parse_data()

    def __len__(self):
        return self._size

    def _parse_data(self):
        if len(self._fmt) > 0:
            with LogicalVolumeFile(self._volume_letter) as volume_file:
                raw_data = volume_file.read(self._base_address, self._size)
                self._data = unpack(self._fmt, raw_data)
        else:
            self._data = None

    @staticmethod
    def _get_size_from_fmt(fmt):
        return fmt.count('B') + 2 * fmt.count('H') + 4 * fmt.count('I') + \
            8 * fmt.count('Q')
