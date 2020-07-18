class LogicalVolumeFile:

    FILE_PATH_FORMAT: str = r'\\.\{}:'

    def __init__(self, volume_letter: str):
        self._letter = volume_letter
        self._path = LogicalVolumeFile.FILE_PATH_FORMAT.format(volume_letter)

    def __enter__(self) -> 'LogicalVolumeFile':
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.close()

    def open(self) -> None:
        try:
            self._file = open(self._path, 'rb')
        except Exception:
            raise IOError(f'Couldn\'t open logical volume '
                          f'{self._letter} file. Make sure the volume '
                          f'exists and that you have administrator permissions'
                          )

    def close(self) -> None:
        self._file.close()

    def seek(self, offset: int) -> None:
        self._file.seek(offset)

    def read(self, size: int) -> bytes:
        data = b''
        while len(data) < size:
            data += self._file.read(size - len(data))
        return data
