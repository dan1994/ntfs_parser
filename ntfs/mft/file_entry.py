from struct import unpack

from ntfs.mft.file_attributes import FileAttributes, FileAttribute
from ntfs.utils.header import MultiHeader, Header
from ntfs.utils import ntfs_logger


class FileEntry(MultiHeader):

    SIZE = 1024

    MAGIC = unpack('I', b'FILE')[0]

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileEntry, self).__init__(volume_letter, base_address)

    def __bool__(self) -> bool:
        return self._header.magic == FileEntry.MAGIC

    @ property
    def path(self) -> str:
        for attribute in self._attributes:
            if attribute.attribute_type == FileAttribute.Type.FILE_NAME:
                return attribute.data().file_name.decode('utf-16')

    @ property
    def file_size(self) -> int:
        return self._header.used_size

    @ property
    def first_attribute_offset(self):
        return self._header.first_attribute_offset

    def _get_next_header_info(self):
        yield FileEntryHeader, self._base_address
        self._header: FileEntryHeader = self._headers.pop(0)

        if not self:
            return

        yield FileAttributes, self._base_address + self.first_attribute_offset
        self._attributes = self._headers.pop(0)


class FileEntryHeader(Header):

    FMT = 'IHHQHHHHIIQHHI'

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileEntryHeader, self).__init__(volume_letter, base_address,
                                              FileEntryHeader.FMT)

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
