
from ntfs import open_ntfs_file


def main(path: str) -> None:
    with open_ntfs_file(path) as ntfs_file:
        print(ntfs_file.read())


if __name__ == "__main__":
    from logging import DEBUG, INFO, WARNING, ERROR
    from argparse import ArgumentParser

    from ntfs.utils import set_ntfs_log_level

    parser = ArgumentParser(
        description='Parse ntfs to retrieve a file\'s content')
    parser.add_argument('file_path')
    parser.add_argument('-v', '--verbose', action='count')
    args = parser.parse_args()

    log_level = {1: WARNING, 2: INFO, 3: DEBUG}.get(args.verbose, ERROR)
    set_ntfs_log_level(log_level)

    main(args.file_path)
