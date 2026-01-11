import logging


class BaseService:
    def __init__(self, service_name: str | None = None) -> None:
        name = service_name or self.__class__.__name__
        self.logger = logging.getLogger(name)
