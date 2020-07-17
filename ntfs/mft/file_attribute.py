from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.utils.header import Header, MultiHeader
from ntfs.utils import ntfs_logger


class FileAttribute(MultiHeader):

    class Type:
        INVALID = 0xffffffff
        FILE_NAME = 0x30
        DATA = 0x80

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileAttribute, self).__init__(volume_letter, base_address)

    def data(self):
        if self.is_resident:
            return self._type_header
        else:
            raise NotImplementedError(
                'Not handling non-resident attribute data yet')

    @ property
    def attribute_type(self):
        return self._constant_header.attribute_type

    @ property
    def is_resident(self):
        return not self._constant_header.non_resident

    def __len__(self):
        return self._constant_header.length

    def _get_next_header_info(self):
        offset = self._base_address
        yield FileAttributeHeader, offset
        self._constant_header = self._headers.pop(0)
        offset += len(self._constant_header)

        if self.attribute_type == FileAttribute.Type.INVALID:
            return

        yield self._residency_dependent_header(), offset
        self._residency_header = self._headers.pop(0)
        offset += len(self._residency_header)

        if not self.is_resident:
            return

        type_dependent_header_type = self._type_dependent_header()
        if type_dependent_header_type is not None:
            yield type_dependent_header_type, offset
            self._type_header = self._headers.pop(0)
            offset += len(self._type_header)

    def _residency_dependent_header(self):
        if self.is_resident:
            return ResidentFileAttributeHeader
        else:
            return NonResidentFileAttributeHeader

    def _type_dependent_header(self):
        if self.attribute_type == FileAttribute.Type.FILE_NAME:
            return FileNameAttributeHeader


class FileAttributeHeader(Header):

    FMT = 'IIBBHHH'

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileAttributeHeader, self).__init__(volume_letter, base_address,
                                                  FileAttributeHeader.FMT)

        self.attribute_type, \
            self.length, \
            self.non_resident, \
            self.name_length, \
            self.name_offset, \
            self.flags, \
            self.attribute_id = self._data


class ResidentFileAttributeHeader(Header):

    FMT = 'IHBB'

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(ResidentFileAttributeHeader, self).\
            __init__(volume_letter, base_address,
                     ResidentFileAttributeHeader.FMT)

        self.attribute_length, \
            self.attribute_offset, \
            self.indexed, \
            self.unused = self._data


class NonResidentFileAttributeHeader(Header):

    FMT = 'QQHHIQQQ'

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(NonResidentFileAttributeHeader, self).\
            __init__(volume_letter, base_address,
                     NonResidentFileAttributeHeader.FMT)

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

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileNameAttributeHeader, self).\
            __init__(volume_letter, base_address, FileNameAttributeHeader.FMT)

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

        with LogicalVolumeFile(self._volume_letter) as volume_file:
            self.file_name = volume_file.read(self._base_address + self._size,
                                              self.file_name_length * 2)
