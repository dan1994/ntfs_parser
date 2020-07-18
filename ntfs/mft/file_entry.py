from struct import unpack

from ntfs.mft.file_attributes import FileAttributes, FileAttribute
from ntfs.utils.header import MultiHeader, Header


class FileEntry(MultiHeader):

    SIZE = 1024

    MAGIC = unpack('I', b'FILE')[0]

    def __bool__(self) -> bool:
        return self._header.magic == FileEntry.MAGIC

    @ property
    def path(self) -> str:
        for attribute in self._attributes:
            if attribute.attribute_type == FileAttribute.Type.FILE_NAME:
                return attribute.data().file_name.decode('utf-16')

    @ property
    def file_size(self) -> int:
        for attribute in self._attributes:
            if attribute.attribute_type == FileAttribute.Type.DATA:
                return attribute.data_size
        return 0

    @ property
    def first_attribute_offset(self):
        return self._header.first_attribute_offset

    def _get_next_header_info(self):
        yield FileEntryHeader, 0
        self._header: FileEntryHeader = self._headers.pop(0)

        if not self:
            return

        yield FileAttributes, self.first_attribute_offset
        self._attributes = self._headers.pop(0)


class FileEntryHeader(Header):

    FMT = 'IHHQHHHHIIQHHI'

    def __init__(self, data, offset):
        super(FileEntryHeader, self).__init__(data, offset)

        self.magic, \
            self.update_sequence_offset, \
            self.update_sequence_size, \
            self.log_sequence, \
            self.sequence_number, \
            self.hard_link_count, \
            self.first_attribute_offset, \
            self.flags, \
            self.used_size, \
            self.allocated_size, \
            self.file_refernce, \
            self.next_attribute_id, \
            self.unused, \
            self.record_number = self._data
