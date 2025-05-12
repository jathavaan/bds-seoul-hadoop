import logging

from dependency_injector import containers, providers

from src.application.common import Logger
from src.application.services.hadoop_service.hdfs_service import HdfsService
from src.application.services.mapreduce_service import MapreduceService
from src.application.services.file_service import FileService


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger.get_logger, name="Hadoop", level=logging.INFO)
    hdfs_service = providers.Singleton(HdfsService, logger=logger)
    mapreduce_service = providers.Singleton(MapreduceService, logger=logger)
    file_service = providers.Singleton(FileService, logger=logger)
