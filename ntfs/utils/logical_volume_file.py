from typing import IO


class LogicalVolumeFile:

    FILE_PATH_FORMAT: str = r'\\.\{}:'

    def __init__(self, volume_letter: str):
        self._letter = volume_letter
        self._path: str = \
            LogicalVolumeFile.FILE_PATH_FORMAT.format(volume_letter)
        self._file: IO[bytes] = None

    def __enter__(self) -> 'LogicalVolumeFile':
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.close()

    def open(self) -> None:
        try:
            self._file: IO[bytes] = open(self._path, 'rb')
        except Exception:
            raise IOError(f'Couldn\'t open logical volume '
                          f'{self._letter} file. Make sure the volume '
                          f'exists and that you have administrator permissions'
                          )

    def close(self) -> None:
        self._file.close()

    def read(self, offset: int, size: int) -> bytes:
        extra_size = (offset % 0x200)
        valid_offset = offset - extra_size
        size_to_read = size + extra_size

        self._file.seek(valid_offset)

        data = b''
        while len(data) < size_to_read:
            data += self._file.read(size_to_read - len(data))
        return data[extra_size:]
