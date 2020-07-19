from ntfs.mft.file_attribute import FileAttribute
from ntfs.utils.header import HeaderList


class FileAttributes(HeaderList):

    HEADER_TYPE = FileAttribute
