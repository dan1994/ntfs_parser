from struct import unpack_from

from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.utils import ntfs_logger


class Vbr:

    SIZE: int = 512

    BPB_OFFSET: int = 0xB
    MFT_CLUSTER_OFFSET: int = 0x30

    def __init__(self, volume_letter: str):
        ntfs_logger.debug(f"{self.__class__}")

        with LogicalVolumeFile(volume_letter) as volume_file:
            raw_data: bytes = volume_file.read(0, Vbr.SIZE)

        self._extract_data(raw_data)

    def get_mft_start_address(self) -> int:
        return self._mft_index * self._cluster_size_in_sectors * \
            self._sector_size_in_bytes

    def _extract_data(self, raw_data: bytes) -> None:
        self._sector_size_in_bytes, self._cluster_size_in_sectors = \
            unpack_from('HB', raw_data, Vbr.BPB_OFFSET)
        self._mft_index = unpack_from('Q', raw_data, Vbr.MFT_CLUSTER_OFFSET)[0]
