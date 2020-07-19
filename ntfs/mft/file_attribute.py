from typing import Type

from ntfs.utils.header import Header, MultiHeader, HeaderGenerator
from ntfs.mft.data_runs import DataRuns


class FileAttribute(MultiHeader):

    class AttrType:
        INVALID = 0xffffffff
        FILE_NAME = 0x30
        DATA = 0x80

    @property
    def is_valid(self) -> bool:
        return self.attribute_type != FileAttribute.AttrType.INVALID

    @property
    def attribute_type(self) -> int:
        return self._constant_header.attribute_type

    @property
    def is_resident(self) -> bool:
        return not self._constant_header.non_resident

    @property
    def data_size(self) -> int:
        if self.is_resident:
            return self._residency_header.attribute_length
        return self._residency_header.attribute_size

    @property
    def data(self) -> Type[Header]:
        if not self.is_resident:
            raise RuntimeError(
                'Can\'t retrieve data of a non-resident attribute')
        return self._type_header.data

    @property
    def data_runs(self) -> DataRuns:
        if self.is_resident:
            raise RuntimeError('Resident attribute doesn\'t have data runs')
        return self._data_runs

    def __len__(self) -> int:
        return self._constant_header.length

    def _get_next_header_info(self) -> HeaderGenerator:
        offset = 0

        yield FileAttributeHeader, offset
        self._constant_header = self._headers.pop(0)
        offset += len(self._constant_header)

        if self.attribute_type == FileAttribute.AttrType.INVALID:
            return

        yield self._residency_dependent_header(), offset
        self._residency_header = self._headers.pop(0)
        offset += len(self._residency_header)

        self._type_header = None
        self._data_runs = None

        if self.is_resident:
            type_dependent_header_type = self._type_dependent_header()
            if type_dependent_header_type is not None:
                yield type_dependent_header_type, offset
                self._type_header = self._headers.pop(0)
                offset += len(self._type_header)
        else:
            yield DataRuns, offset
            self._data_runs = self._headers.pop(0)

    def _residency_dependent_header(self) -> type:
        if self.is_resident:
            return ResidentFileAttributeHeader
        else:
            return NonResidentFileAttributeHeader

    def _type_dependent_header(self) -> type:
        return {
            FileAttribute.AttrType.FILE_NAME: FileNameAttributeHeader,
            FileAttribute.AttrType.DATA: RawData
        }.get(self.attribute_type, None)


class FileAttributeHeader(Header):

    FMT = 'IIBBHHH'

    def __init__(self, data: bytes, offset: int):
        super(FileAttributeHeader, self).__init__(data, offset)

        self.attribute_type, \
            self.length, \
            self.non_resident, \
            self.name_length, \
            self.name_offset, \
            self.flags, \
            self.attribute_id = self._data


class ResidentFileAttributeHeader(Header):

    FMT = 'IHBB'

    def __init__(self, data: bytes, offset: int):
        super(ResidentFileAttributeHeader, self).__init__(data, offset)

        self.attribute_length, \
            self.attribute_offset, \
            self.indexed, \
            self.unused = self._data


class NonResidentFileAttributeHeader(Header):

    FMT = 'QQHHIQQQ'

    def __init__(self, data: bytes, offset: int):
        super(NonResidentFileAttributeHeader, self).__init__(data, offset)

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

    def __init__(self, data: bytes, offset: int):
        super(FileNameAttributeHeader, self).__init__(data, offset)

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

        file_name_offset = offset + len(self)
        file_name_size = self.file_name_length * 2
        self.file_name = \
            data[file_name_offset: file_name_offset + file_name_size].\
            decode('utf-16')

    @property
    def data(self):
        return self.file_name


class RawData:

    def __init__(self, data: bytes, offset: int):
        self._data = data[offset:]

    @property
    def data(self) -> bytes:
        return self._data

    def __len__(self) -> int:
        return len(self._data)
