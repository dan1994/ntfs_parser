from struct import error as struct_error
from typing import List

from ntfs.mft.file_attribute import FileAttribute
from ntfs.utils.header import MultiHeader
from ntfs.utils import ntfs_logger


class FileAttributes(MultiHeader):

    def __init__(self, data, offset):
        try:
            super(FileAttributes, self).__init__(data, offset)
        except struct_error:
            ntfs_logger.warning(
                'Reached end of file entry while parsing attributes')

    def __enter__(self) -> List[FileAttribute]:
        return self._headers

    def __getitem__(self, index: int) -> FileAttribute:
        return self._headers[index]

    def __len__(self) -> int:
        return len(self._headers)

    def _get_next_header_info(self):
        current_offset = 0
        yield FileAttribute, current_offset
        while self._headers[-1].attribute_type != FileAttribute.Type.INVALID:
            current_offset += len(self._headers[-1])
            yield FileAttribute, current_offset
