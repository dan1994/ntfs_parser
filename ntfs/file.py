from ntfs.mft.file_entry import FileEntry


class File:

    def __init__(self, file_entry: str):
        self._file_entry: FileEntry = file_entry

    def __enter__(self) -> 'File':
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.close()

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass

    def read(self, size: int = -1) -> bytes:
        return b''
