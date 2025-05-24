import uuid

from interfaces import base_enum


class TaskStatusEnum(base_enum.ReferenceEnum):
    """
    Enum статусов выполнения задач на конфигурацию
    """

    PENDING = (uuid.UUID("a385655d-fc2e-4baa-9ac6-8ea1306383ff"), "pending")
    ERROR = (uuid.UUID("ed8ce546-8866-4c2c-b294-9216d87a1cba"), "error")
    SUCCESS = (uuid.UUID("30b991d6-fa99-4c16-814b-5ac9c6d131a5"), "success")
