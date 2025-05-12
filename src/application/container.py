import logging

from dependency_injector import containers, providers

from src.application.common import Logger
from src.application.services.hadoop_service.hadooop_service import HadoopService


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger.get_logger, name="Hadoop", level=logging.INFO)
    hadoop_service = providers.Singleton(HadoopService, logger=logger)
