import typing
from ... import types
import datetime


class Attachment(types.OkDeskBaseClass):
    """
    {
      "id": 22,
      "attachment_file_name": "image.jpg",
      "description": "",
      "attachment_file_size": 7955,
      "is_public": true,
      "created_at": "2019-10-29T17:31:30.675+03:00",
      "attachment_url": "https://static.okdesk.ru/attachments/attachments/000/000/150/original/hqdefault.jpg"
    }
    {
      "attachment_file_name": "file.jpg",
      "description": "Описание",
      "is_public": true,
      "id": 575
    }
    """

    def __init__(self):
        self.id: int = None
        self.description: str = None
        self.is_public: bool = None
        self.attachment_file_name: str = None
        self.attachment_file_size: typing.Optional[int] = None
        self.created_at: typing.Optional[datetime.datetime] = None
        self.attachment_url: typing.Optional[str] = None

    @classmethod
    def json_parse(cls, data: dict) -> "Attachment":
        instance = cls()
        instance.id = data.get("id")
        instance.attachment_file_name = data.get("attachment_file_name")
        instance.description = data.get("description")
        instance.attachment_file_size = data.get("attachment_file_size")
        instance.is_public = data.get("is_public")
        created_at = data.get("created_at")
        if created_at:
            instance.created_at = datetime.datetime.fromisoformat(created_at)
        instance.attachment_url = data.get("attachment_url")
        return instance


