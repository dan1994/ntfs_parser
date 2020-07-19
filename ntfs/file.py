from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.mft.file_entry import FileEntry
from ntfs.utils import ntfs_logger


class File:

    def __init__(self, volume_letter: str, cluster_size_in_bytes: int,
                 file_entry: FileEntry):
        self._volume_file = LogicalVolumeFile(volume_letter)
        self._cluster_size_in_bytes = cluster_size_in_bytes
        self._file_entry = file_entry

    def __enter__(self) -> 'File':
        self.open()
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def open(self) -> None:
        self._volume_file.open()

    def close(self) -> None:
        self._volume_file.close()

    def read(self) -> bytes:
        if self._file_entry.is_data_resident:
            ntfs_logger.info('Data is resident in the MFT')
            return self._read_resident_data()

        ntfs_logger.info('Data is not resident in the MFT, finding in disk...')
        return self._read_non_resident_data()

    def _read_resident_data(self) -> bytes:
        return self._file_entry.data

    def _read_non_resident_data(self) -> bytes:
        data = b''
        for offset, length in self._file_entry.data_runs:
            offset_in_bytes = offset * self._cluster_size_in_bytes
            length_in_bytes = length * self._cluster_size_in_bytes

            ntfs_logger.debug(f'Next chunk at {hex(offset_in_bytes)}, with '
                              f'length {hex(length_in_bytes)}')

            self._volume_file.seek(offset_in_bytes)
            data += self._volume_file.read(length_in_bytes)
        return data
