# maintenance entities
import datetime
import os.path
import typing
from requests_toolbelt import MultipartEncoder
import mimetypes
from ... import types
from .. import shared


class MaintanceEntity(types.OkDeskBaseClass):
    """
    {
        "id": 1,
        "name": "Магазин №13",
        "address": null,
        "comment": null,
        "default_assignee_id": 12,
        "default_assignee_group_id": 1,
        "company_id": 1040,
        "timezone": {
          "code": "Moscow",
          "name": "Москва",
          "gmt": "+03:00"
        },
        "contacts_ids": [
          23,
          24,
          63,
          64,
          65
        ],
        "equipments_ids": [
          8,
          9
        ],
        "coordinates": [
          53.2184321,
          44.9998082
        ],
        "parameters": [
          {
            "code": "attr1",
            "name": "Номер документа",
            "field_type": "ftstring",
            "value": "2368590"
          },
          {
            "code": "attr2",
            "name": "Дата начала сотрудничества",
            "field_type": "ftdate",
            "value": "2019-02-06"
          },
          {
            "code": "attr3",
            "name": "Дата следущего созвона",
            "field_type": "ftdatetime",
            "value": "2019-02-21T14:00:00.000+03:00"
          },
          {
            "code": "attr4",
            "name": "Вип обслуживание",
            "field_type": "ftcheckbox",
            "value": true
          },
          {
            "code": "attr5",
            "name": "Вид деятельности",
            "field_type": "ftselect",
            "value": "Программное обеспечение"
          },
          {
            "code": "attr6",
            "name": "Виды помещений",
            "field_type": "ftmultiselect",
            "value": [
              "Главный офис",
              "Зона отдыха"
            ]
          }
        ],
        "schedule": {
          "id": 1,
          "name": "По рабочим дням с 9:00 до 18:00"
        },
        "observers": [
          {
            "id": 5,
            "name": "Иванов Сергей Петрович"
          },
          {
            "id": 12,
            "name": "Петров Иван Валерьевич"
          }
        ],
        "observer_groups": [
          {
            "id": 23,
            "name": "Механики"
          },
          {
            "id": 3,
            "name": "Водители"
          }
        ],
        "attachments": [
          {
            "attachment_file_name": "file.jpg",
            "description": "Описание",
            "is_public": true,
            "id": 575
          }
        ],
        "agreements": [
          {
            "id": 2,
            "title": "Важный Договор"
          }
        ]
      }
    """

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.address: str = None
        self.comment: str = None
        self.default_assignee_id: int = None
        self.default_assignee_group_id: int = None
        self.company_id: int = None
        self.timezone: dict = None
        self.contacts_ids: typing.List[int] = None
        self.equipments_ids: typing.List[int] = None
        self.coordinates: typing.List[float] = None
        self.parameters: typing.List[dict] = None
        self.schedule: types.IdNamePair = None
        self.observers: typing.List[types.IdNamePair] = None
        self.observer_groups: typing.List[types.IdNamePair] = None
        self.attachments: typing.List[shared.Attachment] = None
        self.agreements: typing.List[types.IdNamePair] = None

    @classmethod
    def json_parse(cls, data: dict) -> "MaintanceEntity":
        result = cls()
        result.id = data.get("id")
        result.name = data.get("name")
        result.address = data.get("address")
        result.comment = data.get("comment")
        result.default_assignee_id = data.get("default_assignee_id")
        result.default_assignee_group_id = data.get("default_assignee_group_id")
        result.company_id = data.get("company_id")
        result.timezone = data.get("timezone")
        result.contacts_ids = data.get("contacts_ids")
        result.equipments_ids = data.get("equipments_ids")
        result.coordinates = data.get("coordinates")
        result.parameters = data.get("parameters")
        result.schedule = data.get("schedule")
        result.observers = data.get("observers")
        result.observer_groups = data.get("observer_groups")
        result.attachments = []
        for attachment in data.get("attachments", []):
            result.attachments.append(shared.Attachment.json_parse(attachment))
        if not result.attachments:
            result.attachments = None
        result.agreements = data.get("agreements")
        return result


class CreateMaintenanceEntityRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!obekty-obsluzhivaniya-sozdanie-obekta-obsluzhivaniya

    Название 	                Тип 	            Обязательность 	Описание
    name 	                    string 	            обязательный 	Название объекта обслуживания
    company_id 	                integer 	        обязательный 	ID компании
    agreement_ids 	            array of int 	    необязательный 	ID договоров
    address 	                string 	            необязательный 	Адрес объекта обслуживания. Внимание! При передаче текстовой части адреса автоматическая подстановка координат адреса (геокодинг) не осуществляется. Для того, чтобы адрес отображался на карте, необходимо дополнительно передать координаты адреса в параметре coordinates. Перевести текстовую часть адреса в координаты можно с помощью сервисов геокодинга, например DaData.ru, Google Geocoding API и т.д.
    coordinates 	            array of float 	    необязательный 	Координаты объекта обслуживания
    timezone 	                string 	            необязательный 	Часовой пояс объекта обслуживания
    comment 	                string 	            необязательный 	Дополнительная информация об объекте обслуживания
    default_assignee_id 	    integer 	        необязательный 	ID ответственного по умолчанию
    default_assignee_group_id 	integer 	        необязательный 	ID ответственной группы по умолчанию
    schedule_id 	            integer 	        необязательный 	ID графика работы объекта обслуживания
    observer_ids 	            array of int 	    необязательный 	Массив из ID пользователей, являющихся наблюдателями объекта обслуживания
    observer_group_ids          array of int 	    необязательный 	Массив из ID групп сотрудников, являющихся наблюдателями объекта обслуживания
    custom_parameters 	        associative array 	опционально 	Дополнительные атрибуты объекта обслуживания
    """

    def __init__(
        self,
        name: str,
        company_id: int,
        agreement_ids: typing.Optional[typing.List[int]] = None,
        address: typing.Optional[str] = None,
        coordinates: typing.Optional[typing.List[float]] = None,
        timezone: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        default_assignee_id: typing.Optional[int] = None,
        default_assignee_group_id: typing.Optional[int] = None,
        schedule_id: typing.Optional[int] = None,
        observer_ids: typing.Optional[typing.List[int]] = None,
        observer_group_ids: typing.Optional[typing.List[int]] = None,
        custom_parameters: typing.Optional[dict] = None,
    ):
        """

        :param name: Name of the service object (Имя объекта обслуживания)
        :param company_id:  Company ID (ID компании)
        :param agreement_ids: Agreement IDs (ID договоров)
        :param address: Address of the service object (Адрес объекта обслуживания)
        :param coordinates: Coordinates of the service object (Координаты объекта обслуживания)
        :param timezone: Timezone of the service object (Часовой пояс объекта обслуживания)
        :param comment: Additional information about the service object (Дополнительная информация об объекте обслуживания)
        :param default_assignee_id: Default assignee ID (ID ответственного по умолчанию)
        :param default_assignee_group_id: Default assignee group ID (ID ответственной группы по умолчанию)
        :param schedule_id: Service object schedule ID (ID графика работы объекта обслуживания)
        :param observer_ids: Array of user IDs who are observers of the service object (Массив из ID пользователей, являющихся наблюдателями объекта обслуживания)
        :param observer_group_ids: Array of employee group IDs who are observers of the service object (Массив из ID групп сотрудников, являющихся наблюдателями объекта обслуживания)
        :param custom_parameters: Additional attributes of the service object (Дополнительные атрибуты объекта обслуживания)
        """

        self.name: str = name
        self.company_id: int = company_id
        self.agreement_ids: typing.Optional[typing.List[int]] = agreement_ids
        self.address: typing.Optional[str] = address
        self.coordinates: typing.Optional[typing.List[float]] = coordinates
        self.timezone: typing.Optional[str] = timezone
        self.comment: typing.Optional[str] = comment
        self.default_assignee_id: typing.Optional[int] = default_assignee_id
        self.default_assignee_group_id: typing.Optional[int] = default_assignee_group_id
        self.schedule_id: typing.Optional[int] = schedule_id
        self.observer_ids: typing.Optional[typing.List[int]] = observer_ids
        self.observer_group_ids: typing.Optional[typing.List[int]] = observer_group_ids
        self.custom_parameters: typing.Optional[dict] = custom_parameters

    def to_request(
        self,
    ) -> dict:
        json_data = {
            "name": self.name,
            "company_id": self.company_id,
        }
        if self.agreement_ids is not None:
            json_data["agreement_ids"] = self.agreement_ids
        if self.address is not None:
            json_data["address"] = self.address
        if self.coordinates is not None:
            json_data["coordinates"] = self.coordinates
        if self.timezone is not None:
            json_data["timezone"] = self.timezone
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.default_assignee_id is not None:
            json_data["default_assignee_id"] = self.default_assignee_id
        if self.default_assignee_group_id is not None:
            json_data["default_assignee_group_id"] = self.default_assignee_group_id
        if self.schedule_id is not None:
            json_data["schedule_id"] = self.schedule_id
        if self.observer_ids is not None:
            json_data["observer_ids"] = self.observer_ids
        if self.observer_group_ids is not None:
            json_data["observer_group_ids"] = self.observer_group_ids
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        return {
            "method": "POST",
            "url": "api/v1/maintenance_entities/",
            "json": {"maintenance_entity": json_data},
        }

    def from_response(self, result: dict) -> MaintanceEntity:
        return MaintanceEntity.json_parse(result)


class SearchMaintenanceEntityRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!obekty-obsluzhivaniya-poisk-obekta-obsluzhivaniya

    name            string  (необязательное)    Название объекта обслуживания
    comment         string  (необязательное)    Дополнительная информация об объекте обслуживания
    search_string   string  (необязательное)    Искомая подстрока
    """

    def __init__(
        self,
        name: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        search_string: typing.Optional[str] = None,
    ):
        """

        :param name: Name of the service object (Название объекта обслуживания)
        :param comment: Additional information about the service object (Дополнительная информация об объекте обслуживания)
        :param search_string: Searched substring (Искомая подстрока)
        """
        self.name: typing.Optional[str] = name
        self.comment: typing.Optional[str] = comment
        self.search_string: typing.Optional[str] = search_string

    def to_request(
        self,
    ) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.name is not None:
            params["name"] = self.name
        if self.comment is not None:
            params["comment"] = self.comment
        if self.search_string is not None:
            params["search_string"] = self.search_string
        return {
            "method": "GET",
            "url": "api/v1/maintenance_entities/",
            "params": params,
        }

    def from_response(self, result: dict) -> typing.List[MaintanceEntity]:
        return [MaintanceEntity.json_parse(item) for item in result]


class UpdateMaintenanceEntityRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!obekty-obsluzhivaniya-redaktirovanie-obekta-obsluzhivaniya

    id                          int     (обязательное)      Идентификатор объекта обслуживания
    name                        string  (необязательное)    Название объекта обслуживания
    company_id                  int     (необязательное)    Идентификатор компании
    agreement_ids               array   (необязательное)    Идентификаторы договоров
    address                     string  (необязательное)    Адрес объекта обслуживания
    coordinates                 array   (необязательное)    Координаты объекта обслуживания
    timezone                    string  (необязательное)    Часовой пояс объекта обслуживания
    comment                     string  (необязательное)    Дополнительная информация об объекте обслуживания
    default_assignee_id         int     (необязательное)    Идентификатор ответственного сотрудника
    default_assignee_group_id   int     (необязательное)    Идентификатор ответственной группы
    schedule_id                 int     (необязательное)    Идентификатор графика работы
    observer_ids                array   (необязательное)    Идентификаторы наблюдателей
    observer_group_ids          array   (необязательное)    Идентификаторы групп наблюдателей
    custom_parameters            array  (необязательное)    Дополнительные атрибуты объекта обслуживания
    """

    def __init__(
        self,
        id_: int,
        name: typing.Optional[str] = None,
        company_id: typing.Optional[int] = None,
        agreement_ids: typing.Optional[typing.List[int]] = None,
        address: typing.Optional[str] = None,
        coordinates: typing.Optional[typing.List[float]] = None,
        timezone: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        default_assignee_id: typing.Optional[int] = None,
        default_assignee_group_id: typing.Optional[int] = None,
        schedule_id: typing.Optional[int] = None,
        observer_ids: typing.Optional[typing.List[int]] = None,
        observer_group_ids: typing.Optional[typing.List[int]] = None,
        custom_parameters: typing.Optional[typing.List[dict]] = None,
    ):
        """

        :param id_: Maintenance entity id (Идентификатор объекта обслуживания)
        :param name: Name (Название объекта обслуживания)
        :param company_id: Company id (Идентификатор компании)
        :param agreement_ids: Agreement ids (Идентификаторы договоров)
        :param address: Address (Адрес объекта обслуживания)
        :param coordinates: Coordinates (Координаты объекта обслуживания)
        :param timezone: Timezone (Часовой пояс объекта обслуживания)
        :param comment: Comment (Дополнительная информация об объекте обслуживания)
        :param default_assignee_id: Default assignee id (Идентификатор ответственного сотрудника)
        :param default_assignee_group_id: Default assignee group id (Идентификатор ответственной группы)
        :param schedule_id: Schedule id (Идентификатор графика работы)
        :param observer_ids: Observer ids (Идентификаторы наблюдателей)
        :param observer_group_ids: Observer group ids (Идентификаторы групп наблюдателей)
        :param custom_parameters: Custom parameters (Дополнительные атрибуты объекта обслуживания)
        """
        self.id: int = id_
        self.name: typing.Optional[str] = name
        self.company_id: typing.Optional[int] = company_id
        self.agreement_ids: typing.Optional[typing.List[int]] = agreement_ids
        self.address: typing.Optional[str] = address
        self.coordinates: typing.Optional[typing.List[float]] = coordinates
        self.timezone: typing.Optional[str] = timezone
        self.comment: typing.Optional[str] = comment
        self.default_assignee_id: typing.Optional[int] = default_assignee_id
        self.default_assignee_group_id: typing.Optional[int] = default_assignee_group_id
        self.schedule_id: typing.Optional[int] = schedule_id
        self.observer_ids: typing.Optional[typing.List[int]] = observer_ids
        self.observer_group_ids: typing.Optional[typing.List[int]] = observer_group_ids
        self.custom_parameters: typing.Optional[typing.List[dict]] = custom_parameters

    def to_request(
        self,
    ) -> dict:
        json_data = {
            "id": self.id,
        }
        if self.name is not None:
            json_data["name"] = self.name
        if self.company_id is not None:
            json_data["company_id"] = self.company_id
        if self.agreement_ids is not None:
            json_data["agreement_ids"] = self.agreement_ids
        if self.address is not None:
            json_data["address"] = self.address
        if self.coordinates is not None:
            json_data["coordinates"] = self.coordinates
        if self.timezone is not None:
            json_data["timezone"] = self.timezone
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.default_assignee_id is not None:
            json_data["default_assignee_id"] = self.default_assignee_id
        if self.default_assignee_group_id is not None:
            json_data["default_assignee_group_id"] = self.default_assignee_group_id
        if self.schedule_id is not None:
            json_data["schedule_id"] = self.schedule_id
        if self.observer_ids is not None:
            json_data["observer_ids"] = self.observer_ids
        if self.observer_group_ids is not None:
            json_data["observer_group_ids"] = self.observer_group_ids
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        return {
            "method": "PATCH",
            "url": f"api/v1/maintenance_entities/{self.id}",
            "json": json_data,
        }

    def from_response(self, result) -> MaintanceEntity:
        return MaintanceEntity.json_parse(result)


class GetMaintenanceEntityRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!informacziya-ob-obekte-obsluzhivaniya-informacziya-ob-obekte-obsluzhivaniya

    Получение информации об объекте обслуживания

    """

    def __init__(self, id_: int):
        """

        :param id_: Id (Идентификатор объекта обслуживания)
        """
        self.id: int = id_

    def to_request(
        self,
    ) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/maintenance_entities/{self.id}",
        }

    def from_response(self, result) -> MaintanceEntity:
        return MaintanceEntity.json_parse(result)


class ListMaintenanceEntitiesRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-obektov-obsluzhivaniya-poluchenie-spiska-po-parametram

    Название 	                Тип 	            Обязательность 	Описание
    company_ids 	            array of integer 	опционально 	Массив из ID компаний.
    Пример: company_ids[]=1

    default_assignee_ids 	    array of integer 	опционально 	Массив из ID ответственных (для отображения объектов обслуживания без ответственного необходимо передавать в параметре значение “0”).
    Пример: default_assignee_ids[]=1

    default_assignee_group_ids 	array of integer 	опционально 	Массив из ID ответственных групп (для отображения объектов обслуживания без ответственной группы необходимо передавать в параметре значение “0”).
    Пример: default_assignee_group_ids[]=1

    created_since 	            string 	            опционально 	Дата создания объектов обслуживания в часовом поясе аккаунта (С)
    Пример: created_since=2019-05-25

    created_until 	            string 	            опционально 	Дата создания объектов обслуживания в часовом поясе аккаунта (По)
    Пример: created_until=2019-05-25

    updated_since 	            string 	            опционально 	Дата изменения объектов обслуживания в часовом поясе аккаунта (С)
    Пример: updated_since=2019-05-25

    updated_until 	            string 	            опционально 	Дата изменения объектов обслуживания в часовом поясе аккаунта (По)
    Пример: updated_until=2019-05-25

    page 	                    associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка объектов обслуживания (подробное описание представлено в таблице ниже).

    =================================
    Допустимые параметры постраничного вывода:

    Название 	Тип значения 	Обязательность 	Описание
    size 	    integer 	    опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	    опционально 	D объекта обслуживания, с которого начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id объекта.
    Пример: page[from_id]=10

    direction 	string 	        опционально 	Направление выборки.
    Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id объекта.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id объекта.
    Пример: page[direction]=forward

    """

    def __init__(
        self,
        company_ids: typing.Optional[typing.List[int]] = None,
        default_assignee_ids: typing.Optional[typing.List[int]] = None,
        default_assignee_group_ids: typing.Optional[typing.List[int]] = None,
        created_since: typing.Optional[datetime.date] = None,
        created_until: typing.Optional[datetime.date] = None,
        updated_since: typing.Optional[datetime.date] = None,
        updated_until: typing.Optional[datetime.date] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param company_ids: Company IDs (ID компаний)
        :param default_assignee_ids: Default assignee IDs (ID ответственных по умолчанию)
        :param default_assignee_group_ids: Default assignee group IDs (ID групп ответственных по умолчанию)
        :param created_since: Created since (Созданы с)
        :param created_until: Created until (Созданы по)
        :param updated_since: Updated since (Обновлены с)
        :param updated_until: Updated until (Обновлены по)
        :param page_size: Page size (Число возвращаемых записей)
        :param page_from_id: Page from id (D объекта обслуживания, с которого начинается выборка записей)
        :param page_direction: Page direction (Направление выборки)
        """

        self.company_ids: typing.Optional[typing.List[int]] = company_ids
        self.default_assignee_ids: typing.Optional[
            typing.List[int]
        ] = default_assignee_ids
        self.default_assignee_group_ids: typing.Optional[
            typing.List[int]
        ] = default_assignee_group_ids
        self.created_since: typing.Optional[datetime.date] = created_since
        self.created_until: typing.Optional[datetime.date] = created_until
        self.updated_since: typing.Optional[datetime.date] = updated_since
        self.updated_until: typing.Optional[datetime.date] = updated_until
        self.page_size: typing.Optional[int] = page_size
        self.page_from_id: typing.Optional[int] = page_from_id
        self.page_direction: typing.Optional[
            typing.Literal["reverse", "forward"]
        ] = page_direction

    def to_request(
        self,
    ) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.company_ids is not None:
            params["company_ids"] = []
            for item in self.company_ids:
                params["company_ids"].append(str(item))
        if self.default_assignee_ids is not None:
            params["default_assignee_ids"] = []
            for item in self.default_assignee_ids:
                params["default_assignee_ids"].append(str(item))
        if self.default_assignee_group_ids is not None:
            params["default_assignee_group_ids"] = []
            for item in self.default_assignee_group_ids:
                params["default_assignee_group_ids"].append(str(item))
        if self.created_since is not None:
            params["created_since"] = self.created_since.strftime("%Y-%m-%d")
        if self.created_until is not None:
            params["created_until"] = self.created_until.strftime("%Y-%m-%d")
        if self.updated_since is not None:
            params["updated_since"] = self.updated_since.strftime("%Y-%m-%d")
        if self.updated_until is not None:
            params["updated_until"] = self.updated_until.strftime("%Y-%m-%d")
        if self.page_size is not None:
            params["page[size]"] = str(self.page_size)
        if self.page_from_id is not None:
            params["page[from_id]"] = str(self.page_from_id)
        if self.page_direction is not None:
            params["page[direction]"] = self.page_direction
        return {
            "method": "GET",
            "url": "api/v1/maintenance_entities/list",
            "params": params,
        }

    def from_response(self, result) -> typing.List[MaintanceEntity]:
        return [MaintanceEntity.json_parse(item) for item in result]


class AddMaintenanceEntityAttachmentRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!dobavleniya-fajla-k-obektu-obsluzhivaniya-dobavleniya-fajla-k-obektu-obsluzhivaniya

    Название 	    Тип 	Обязательность 	Описание
    attachments 	array 	обязательный 	Список приложенных файлов
    """

    def __init__(
        self, maintenance_entity_id: int, attachments: typing.List[types.Attachment]
    ):
        """

        :param maintenance_entity_id: Maintenance entity ID (ID объекта обслуживания)
        :param attachments:  (Список приложенных файлов)
        """
        self.maintenance_entity_id = maintenance_entity_id
        self.attachments: typing.List[types.Attachment] = attachments

    def to_request(self) -> dict:
        multipart_data = MultipartEncoder({})
        for i, attachment in enumerate(self.attachments):
            if not os.path.isfile(attachment["attachment"]):
                raise Exception("File not found")
            file_name = os.path.basename(attachment["attachment"])
            content_type = mimetypes.guess_type(file_name)[0]
            multipart_data.fields[
                f"maintenance_entity[attachments][{i}][attachment]"
            ] = (file_name, open(attachment["attachment"], "rb"), content_type)
            if "is_public" in attachment:
                multipart_data.fields[
                    f"maintenance_entity[attachments][{i}][is_public]"
                ] = attachment["is_public"]
            if "description" in attachment:
                multipart_data.fields[
                    f"maintenance_entity[attachments][{i}][description]"
                ] = attachment["description"]

        return {
            "method": "POST",
            "url": f"api/v1/maintenance_entities/{self.maintenance_entity_id}/attachments/",
            "data": multipart_data.read(),
            "headers": {"Content-Type": multipart_data.content_type},
        }

    def from_response(self, result) -> MaintanceEntity:
        return MaintanceEntity.json_parse(result)
