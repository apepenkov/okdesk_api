import typing


class OkDeskBaseClass:
    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            + ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            + ")"
        )

    @classmethod
    def json_parse(cls, data: dict) -> "OkDeskBaseClass":
        raise NotImplementedError


class ApiRequest:
    # method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH"], url: str, **kwargs
    def to_request(self) -> dict:
        raise NotImplementedError

    def from_response(self, result) -> typing.Any:
        raise NotImplementedError


"""
The following types are used when MAKING requests to the API.
Those are dicts with typehints.

When receiving responses from the API, the types are used from api/<endpoint>.py, and are classes.
=====================
Следующие типы используются при ОТПРАВКЕ запросов к API.
Это словари с typehints.

При получении ответов от API используются типы из okdesk_api/api/<category>/, являющиеся классами.
"""


class IdNamePair(typing.TypedDict):
    """{
        "id": 1,
        "name": "Иванов Иван Викторович"
    }"""

    id: int
    name: str


class Category(typing.TypedDict):
    """
    {
        "id": 3,
        "code": "vipclient",
        "name": "VIP-клиент",
        "color": "#5cb85c"
    }"""

    id: int
    code: str
    name: str
    color: str


class Attachment(typing.TypedDict):
    """
    Название 	    Тип 	    Обязательность 	Описание
    attachment 	    string 	    обязательный 	Прикрепляемый файл
    description 	string 	    опционально 	Описание файла
    is_public 	    boolean 	опционально 	Публичность файла
    """

    attachment: str
    description: typing.NotRequired[str]
    is_public: typing.NotRequired[bool]


class CodeNamePair(typing.TypedDict):
    """{
        "code": "vipclient",
        "name": "VIP-клиент"
    }"""

    code: str
    name: str


class IdValuePair(typing.TypedDict):
    """{
        "id": 1,
        "value": "Иванов Иван Викторович"
    }"""

    id: int
    value: str


class IdNameTypePair(typing.TypedDict):
    """{
        "id": 1,
        "name": "Иванов Иван Викторович",
        "type": "user"
    }"""

    id: int
    name: str
    type: str


class CodeIdNamePair(typing.TypedDict):
    """{
        "code": "vipclient",
        "id": 3,
        "name": "VIP-клиент"
    }"""

    code: str
    id: int
    name: str
