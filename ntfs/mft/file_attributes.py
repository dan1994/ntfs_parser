from typing import List

from ntfs.mft.file_attribute import FileAttribute
from ntfs.utils.header import MultiHeader
from ntfs.utils import ntfs_logger


class FileAttributes(MultiHeader):

    def __init__(self, volume_letter, base_address):
        ntfs_logger.debug(f"{self.__class__}, {hex(base_address)}")

        super(FileAttributes, self).__init__(volume_letter, base_address)

    def __enter__(self) -> List[FileAttribute]:
        return self._headers

    def __getitem__(self, index: int) -> FileAttribute:
        return self._headers[index]

    def __len__(self) -> int:
        return len(self._headers)

    def _get_next_header_info(self):
        current_offset = self._base_address
        yield FileAttribute, current_offset
        while self._headers[-1].attribute_type != FileAttribute.Type.INVALID:
            current_offset += len(self._headers[-1])
            yield FileAttribute, current_offset
