from struct import unpack

from ntfs.mft.file_attributes import FileAttributes, FileAttribute
from ntfs.utils.header import MultiHeader, Header, HeaderGenerator
from ntfs.mft.data_runs import DataRuns


class FileEntry(MultiHeader):

    SIZE = 1024

    MAGIC = unpack('I', b'FILE')[0]

    def __init__(self, data: bytes, offset: int):
        super(FileEntry, self).__init__(data, offset)

        self._identify_attributes()

    @property
    def is_valid(self) -> bool:
        return self._header.magic == FileEntry.MAGIC

    @property
    def name(self) -> str:
        if self._name_attribute is None:
            return ''
        return self._name_attribute.data

    @property
    def size(self) -> int:
        if self._data_attribute is None:
            return 0
        return self._data_attribute.data_size

    @property
    def is_data_resident(self) -> bool:
        return self._data_attribute.is_resident

    @property
    def data(self) -> bytes:
        return self._data_attribute.data

    @property
    def data_runs(self) -> DataRuns:
        return self._data_attribute.data_runs

    def _identify_attributes(self) -> None:
        self._name_attribute = None
        self._data_attribute = None

        if not self.is_valid:
            return

        for attribute in self._attributes:
            if attribute.attribute_type == FileAttribute.AttrType.FILE_NAME:
                self._name_attribute = attribute
            if attribute.attribute_type == FileAttribute.AttrType.DATA:
                self._data_attribute = attribute

    def _get_next_header_info(self) -> HeaderGenerator:
        yield FileEntryHeader, 0
        self._header = self._headers.pop(0)

        if not self.is_valid:
            return

        yield FileAttributes, self._header.first_attribute_offset
        self._attributes = self._headers.pop(0)


class FileEntryHeader(Header):

    FMT = 'IHHQHHHHIIQHHI'

    def __init__(self, data: bytes, offset: int):
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
