from ntfs.logical_volume import LogicalVolume
from ntfs.file import File


def open_ntfs_file(volume_letter: str, file_name: str) -> File:
    logical_volume = LogicalVolume(volume_letter)
    return logical_volume.get_file(file_name)
