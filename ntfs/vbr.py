from struct import unpack_from

from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.utils import ntfs_logger


class Vbr:

    SIZE = 512

    BPB_OFFSET = 0xB
    MFT_CLUSTER_OFFSET = 0x30

    def __init__(self, volume_letter: str):
        ntfs_logger.debug(f"{self.__class__}")

        with LogicalVolumeFile(volume_letter) as volume_file:
            raw_data = volume_file.read(Vbr.SIZE)

        self.sector_size_in_bytes, self.cluster_size_in_sectors = \
            unpack_from('=HB', raw_data, Vbr.BPB_OFFSET)
        self.mft_index = unpack_from('=Q', raw_data, Vbr.MFT_CLUSTER_OFFSET)[0]

        ntfs_logger.info(f'Sector size in bytes: {self.sector_size_in_bytes}')
        ntfs_logger.info(f'Cluster size in sectors: '
                         f'{self.cluster_size_in_sectors}')
