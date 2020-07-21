from ntfs.utils.logical_volume_file import LogicalVolumeFile


class VolumeInfo:

    def __init__(self, volume_letter: str, sector_size_in_bytes: int,
                 cluster_size_in_sectors: int):
        self._volume_letter = volume_letter
        self._sector_size_in_bytes = sector_size_in_bytes
        self._cluster_size_in_bytes = cluster_size_in_sectors * \
            sector_size_in_bytes

    def get_volume_file(self) -> LogicalVolumeFile:
        return LogicalVolumeFile(self._volume_letter)

    @property
    def volume_letter(self) -> str:
        return self._volume_letter

    @property
    def sector_size_in_bytes(self) -> int:
        return self._sector_size_in_bytes

    @property
    def cluster_size_in_bytes(self) -> int:
        return self._cluster_size_in_bytes
