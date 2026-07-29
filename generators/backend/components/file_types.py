from enum import Enum


class BackendFileType(str, Enum):

    MODEL = "model"

    SCHEMA = "schema"

    REPOSITORY = "repository"

    SERVICE = "service"

    API = "api"