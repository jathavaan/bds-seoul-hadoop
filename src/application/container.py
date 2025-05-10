import logging

from dependency_injector import containers, providers

from src.application.common import Logger


class Container(containers.DeclarativeContainer):
    logger = providers.Factory(Logger.get_logger, name="Hadoop", level=logging.INFO)
