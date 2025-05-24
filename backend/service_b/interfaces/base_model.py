from pydantic import BaseModel, ConfigDict  # noqa


class ConfigMixin:
    """
    Миксин конфига для DTO
    """

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
