from os.path import splitdrive


from ntfs.logical_volume import LogicalVolume
from ntfs.file import File


def open_ntfs_file(path: str) -> File:
    volume_letter: str = _splitdrive_and_validate(path)
    logical_volume: LogicalVolume = LogicalVolume(volume_letter)
    file_object: File = logical_volume.get_file(path)
    file_object.open()
    return file_object


def _splitdrive_and_validate(path: str) -> str:
    volume_name, _ = splitdrive(path)

    if len(volume_name) == 0:
        raise ValueError('An absolute path is required')

    return volume_name[0]
