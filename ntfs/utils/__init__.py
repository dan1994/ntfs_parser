from logging import getLogger, StreamHandler, Formatter, NOTSET


ntfs_logger = getLogger('NTFS')
ntfs_handler = StreamHandler()
ntfs_formatter = Formatter(
    '[%(asctime)s] %(name)s:%(levelname)s:%(message)s')
ntfs_handler.setFormatter(ntfs_formatter)
ntfs_logger.addHandler(ntfs_handler)
ntfs_logger.setLevel(NOTSET)


def set_ntfs_log_level(log_level: int) -> None:
    global ntfs_logger
    ntfs_logger.setLevel(log_level)


__all__ = [set_ntfs_log_level]
