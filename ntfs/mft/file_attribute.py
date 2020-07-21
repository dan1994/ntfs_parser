from typing import Type

from ntfs.utils.volume_info import VolumeInfo
from ntfs.mft.data_runs import DataRuns
from ntfs.utils.header import Header


class FileAttribute:

    class AttrType:
        INVALID = 0xffffffff
        FILE_NAME = 0x30
        DATA = 0x80

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        self._volume_info = volume_info
        self._parse(data)

    @property
    def is_valid(self) -> bool:
        return self.attribute_type != FileAttribute.AttrType.INVALID

    @property
    def attribute_type(self) -> int:
        return self._constant_header.attribute_type

    @property
    def is_resident(self) -> bool:
        return not self._constant_header.non_resident

    def data(self) -> bytes:
        if self.is_resident:
            raw_data = self._resident_data
        else:
            raw_data = self._data_runs.data()
        return self._type_dependent_header(raw_data).data()

    def __len__(self) -> int:
        return self._constant_header.length

    def _parse(self, data) -> None:
        self._constant_header = FileAttributeHeader(self._volume_info, data)
        offset = len(self._constant_header)

        if not self.is_valid:
            return

        self._parse_residency_header(data[offset:])
        offset += len(self._residency_header)

        if self.is_resident:
            offset = self._residency_header.attribute_offset
            length = self._residency_header.attribute_length
            self._resident_data = data[offset: offset + length]
        else:
            self._data_runs = DataRuns(self._volume_info, data[offset:])

    def _parse_residency_header(self, data) -> None:
        if self.is_resident:
            self._residency_header = \
                ResidentFileAttributeHeader(self._volume_info, data)
        else:
            self._residency_header = \
                NonResidentFileAttributeHeader(self._volume_info, data)

    def _type_dependent_header(self, data) -> Type[Header]:
        return {
            FileAttribute.AttrType.FILE_NAME: FileNameAttributeHeader,
            FileAttribute.AttrType.DATA: RawData
        }.get(self.attribute_type, RawData)(self._volume_info, data)


class FileAttributeHeader(Header):

    FMT = 'IIBBHHH'

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        super(FileAttributeHeader, self).__init__(volume_info, data)

        self.attribute_type, \
            self.length, \
            self.non_resident, \
            self.name_length, \
            self.name_offset, \
            self.flags, \
            self.attribute_id = self._data


class ResidentFileAttributeHeader(Header):

    FMT = 'IHBB'

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        super(ResidentFileAttributeHeader, self).__init__(volume_info, data)

        self.attribute_length, \
            self.attribute_offset, \
            self.indexed, \
            self.unused = self._data


class NonResidentFileAttributeHeader(Header):

    FMT = 'QQHHIQQQ'

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        super(NonResidentFileAttributeHeader, self).__init__(volume_info, data)

        self.first_cluster, \
            self.last_cluster, \
            self.data_run_offset, \
            self.compression_unit, \
            self.unused, \
            self.attribute_allocated, \
            self.attribute_size, \
            self.stream_data_size = self._data


class FileNameAttributeHeader(Header):

    FMT = 'IHHQQQQQQIIBB'

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        super(FileNameAttributeHeader, self).__init__(volume_info, data)

        self.parent_record_number1, \
            self.parent_record_number2, \
            self.sequence_number, \
            self.creation_time, \
            self.modification_time, \
            self.metadata_modification_time, \
            self.read_time, \
            self.allocated_size, \
            self.real_size, \
            self.flags, \
            self.repase, \
            self.file_name_length, \
            self.namespace_type = self._data

        file_name_offset = len(self)
        file_name_size = self.file_name_length * 2
        self.file_name = \
            data[file_name_offset: file_name_offset + file_name_size].\
            decode('utf-16')

    def data(self):
        return self.file_name


class RawData:

    def __init__(self, volume_info: VolumeInfo, data: bytes):
        self._data = data

    def data(self) -> bytes:
        return self._data

    def __len__(self) -> int:
        return len(self._data)
