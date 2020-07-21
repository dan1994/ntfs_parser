from ntfs.utils.logical_volume_file import LogicalVolumeFile
from ntfs.utils.header import Header
from ntfs.utils import ntfs_logger


class Vbr(Header):

    SIZE = 512

    FMT = 'HBQHBHHBHBHHHIIIQQQIBHBQI'

    def __init__(self, data: bytes):
        super(Vbr, self).__init__(None, data)

        self.jump_instruction1, \
            self.jump_instruction2, \
            self.oem_id, \
            self.sector_size_in_bytes, \
            self.cluster_size_in_sectors, \
            self.reserved_sectors, \
            self.zero1, \
            self.zero2, \
            self.unused1, \
            self.media_descriptor, \
            self.zero3,\
            self.sectors_per_track, \
            self.number_of_heads, \
            self.hidden_sectors, \
            self.unused2, \
            self.unused3, \
            self.total_sectors, \
            self.mft_logical_cluster_number, \
            self.mft_mirr_logical_cluster_number, \
            self.clusters_per_file_record_segment, \
            self.clusters_per_index_buffer, \
            self.unused4, \
            self.unused5, \
            self.volume_serial_number, \
            self.checksum = self._data

        ntfs_logger.info(f'Sector size in bytes: {self.sector_size_in_bytes}')
        ntfs_logger.info(f'Cluster size in sectors: '
                         f'{self.cluster_size_in_sectors}')

    @staticmethod
    def read_vbr(volume_letter):
        with LogicalVolumeFile(volume_letter) as volume_file:
            return Vbr(volume_file.read(Vbr.SIZE))
