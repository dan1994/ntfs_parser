from struct import unpack

from ntfs.mft.file_attributes import FileAttributes, FileAttribute
from ntfs.utils.volume_info import VolumeInfo
from ntfs.mft.data_runs import DataRuns
from ntfs.utils.header import Header


class FileEntry:

    SIZE = 1024

    MAGIC = unpack('I', b'FILE')[0]

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        self._volume_info = volume_info
        self._parse(data)

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

    def _parse(self, data: bytes) -> None:
        self._header = FileEntryHeader(self._volume_info, data)

        if not self.is_valid:
            return

        data = data[self._header.first_attribute_offset:]

        self._attributes = FileAttributes(self._volume_info, data)
        self._identify_attributes()

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


class FileEntryHeader(Header):

    FMT = 'IHHQHHHHIIQHHI'

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        super(FileEntryHeader, self).__init__(volume_info, data)

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
