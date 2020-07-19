from sys import byteorder

from ntfs.utils.header import Header


class DataRunHeader(Header):

    FMT = 'B'

    def __init__(self, data: bytes, offset: int):
        super(DataRunHeader, self).__init__(data, offset)

        self.length_field_bytes = self._data[0] & 0x0f
        self.offset_field_bytes = self._data[0] >> 4

        if not self.is_valid:
            self.length = 0
            self.offset = 0
            return

        length_field_start = offset + 1
        length_field_end = length_field_start + self.length_field_bytes
        offset_field_start = length_field_end
        offset_field_end = offset_field_start + self.offset_field_bytes

        length_field = data[length_field_start: length_field_end]
        offset_field = data[offset_field_start: offset_field_end]

        self.length = int.from_bytes(length_field, byteorder)
        self.offset = int.from_bytes(offset_field, byteorder)

    @property
    def is_valid(self) -> bool:
        return self.length_field_bytes != 0 and \
            self.length_field_bytes + self.offset_field_bytes <= 8

    def __len__(self) -> int:
        return 1 + self.length_field_bytes + self.offset_field_bytes