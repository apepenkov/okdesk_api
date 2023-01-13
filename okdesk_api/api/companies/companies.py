from ... import types
import datetime
import typing
from .. import shared
from ... import helpers

"""Компании ¶
Поиск компании
GET
/api/v1/companies/{?api_token,name,phone,id,crm_1c_id,search_string}

Поиск осуществляется по точному совпадению названия или дополнительного названия компании, телефона, внутреннего ID, идентификатора объекта в 1С или по подстроке
Ограничения прав доступа ¶

Поиск компании будет выполнен только в том случае, если связанный с ключом сотрудник имеет доступ к списку компаний в соответствии с настройками прав доступа. Для ключей, связанных с контактными лицами, данный метод недоступен.
Обратите внимание ¶

    При передаче параметра search_string остальные параметры не учитываются

    Символ + в поисковой строке можно использовать только в закодированном варианте %2B, иначе он будет воспринят как пробел

Пример URI
GET https://<account>.okdesk.ru/api/v1/companies/?api_token=3e9a214215f493c4&name=Okdesk&phone=+7(499)703-47-20&id=1040&crm_1c_id=35067c4b23a8&search_string=desk
Параметры URI
Скрыть

api_token
    string (обязательное) Пример: 3e9a214215f493c4

    Ключ авторизации.
name
    string (необязательное) Пример: Okdesk

    Имя компании
phone
    string (необязательное) Пример: +7(499)703-47-20

    Телефон компании
id
    integer (необязательное) Пример: 1040

    Внутренний ID компании
crm_1c_id
    string (необязательное) Пример: 35067c4b23a8

    Идентификатор объекта в 1С
search_string
    string (необязательное) Пример: desk

    Искомая подстрока

Ответ  200
Скрыть
Заголовки

Content-Type: application/json

Тело

{
  "id": 1040,
  "name": "Okdesk",
  "additional_name": "Help Desk система для сервисных компаний",
  "site": "http://okdesk.ru",
  "email": "info@okdesk.ru",
  "phone": "+7(499)703-47-20",
  "crm_1c_id": "35067c4b23a8",
  "active": true,
  "address": "г. Москва, ул. Хелпдескрешений 11, офис 330",
  "comment": "Okdesk — простая и удобная облачная Help Desk система для автоматизации процессов поддержки в малых и средних сервисных компаниях. Позволяет вести учет заявок в службу поддержки, клиентов и всех взаимодействий с ними, условий предоставления услуг (SLA), договоров, их сроков действия и этапов оплаты.",
  "coordinates": [
    53.2184321,
    44.9998082
  ],
  "observers": [
    {
      "id": 2,
      "name": "Эрдингтон Филлип Витальевич"
    },
    {
      "id": 1,
      "name": "Иванов Иван Викторович"
    }
  ],
  "contacts": [],
  "default_assignee": {
    "id": 1,
    "name": "Иванов Иван Викторович"
  },
  "category": {
    "id": 3,
    "code": "vipclient",
    "name": "VIP-клиент",
    "color": "#5cb85c"
  },
  "attachments": [
    {
      "id": 8,
      "attachment_file_name": "photo.jpg",
      "description": "Фотография неисправности",
      "attachment_file_size": 4149,
      "is_public": false,
      "created_at": "2016-09-30T09:28:50.499+03:00"
    }
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
  ]
}"""


class Company(types.OkDeskBaseClass):
    """https://okdesk.ru/apidoc#!kompanii-poisk-kompanii"""

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.additional_name: str = None
        self.site: str = None
        self.email: str = None
        self.phone: str = None
        self.crm_1c_id: str = None
        self.active: bool = None
        self.address: str = None
        self.comment: str = None
        self.coordinates: typing.List[float] = None
        self.observers: typing.List[types.IdNamePair] = None
        self.contacts: list = None
        self.default_assignee: types.IdNamePair = None
        self.category: types.Category = None
        self.attachments: typing.List[shared.Attachment] = None
        self.parameters: typing.List[dict] = None

    @classmethod
    def json_parse(cls, dict_data: dict) -> "Company":
        new_instance = cls()
        new_instance.id = dict_data.get("id")
        new_instance.name = dict_data.get("name")
        new_instance.additional_name = dict_data.get("additional_name")
        new_instance.site = dict_data.get("site")
        new_instance.email = dict_data.get("email")
        new_instance.phone = dict_data.get("phone")
        new_instance.crm_1c_id = dict_data.get("crm_1c_id")
        new_instance.active = dict_data.get("active")
        new_instance.address = dict_data.get("address")
        new_instance.comment = dict_data.get("comment")
        new_instance.coordinates = dict_data.get("coordinates")
        new_instance.observers = dict_data.get("observers")
        new_instance.contacts = dict_data.get("contacts")
        new_instance.default_assignee = dict_data.get("default_assignee")
        new_instance.category = dict_data.get("category")
        for attachment in dict_data.get("attachments", []):
            new_instance.attachments.append(shared.Attachment.json_parse(attachment))
        if not new_instance.attachments:
            new_instance.attachments = None
        new_instance.parameters = dict_data.get("parameters")
        return new_instance


class FindCompanyRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!kompanii-poisk-kompanii
    name            string  Имя компании
    phone           string  Телефон компании
    id              int     Внутренний ID компании
    crm_1c_id       string  ID компании в 1С
    search_string   string  Искомая подстрока

    """

    def __init__(
        self,
        name: typing.Optional[str] = None,
        phone: typing.Optional[str] = None,
        id_: typing.Optional[int] = None,
        crm_1c_id: typing.Optional[str] = None,
        search_string: typing.Optional[str] = None,
    ):
        """
        Поиск осуществляется по точному совпадению названия или дополнительного названия компании,
        телефона, внутреннего ID, идентификатора объекта в 1С или по подстроке

        При передаче параметра search_string остальные параметры не учитываются

        :param name: Имя компании
        :param phone: Телефон компании
        :param id_: Внутренний ID компании
        :param crm_1c_id: ID компании в 1С
        :param search_string: Искомая подстрока
        """
        self.name = name
        self.phone = phone
        self.id = id_
        self.crm_1c_id = crm_1c_id
        self.search_string = search_string

    def to_request(self) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.name:
            params["name"] = self.name
        if self.phone:
            params["phone"] = self.phone
        if self.id:
            params["id"] = self.id
        if self.crm_1c_id:
            params["crm_1c_id"] = self.crm_1c_id
        if self.search_string:
            params["search_string"] = self.search_string
        return {"method": "GET", "url": "api/v1/companies/", "params": params}

    def from_response(self, response: dict) -> Company:
        return Company.json_parse(response)


class CreateCompanyRequest(types.ApiRequest):
    """Создание компании
    https://okdesk.ru/apidoc#!kompanii-sozdanie-kompanii

    POST /api/v1/companies/
    Допустимые параметры запроса: ¶
    Название 	            Тип 	            Обязательность 	Описание
    name 	                string 	            обязательный 	Название компании
    additional_name 	    string 	            необязательный 	Дополнительное название компании
    site 	                string 	            необязательный 	Сайт компании
    email 	                string 	            необязательный 	Контактный E-mail компании
    phone 	                string 	            необязательный 	Контактный телефон компании
    address         	    string 	            необязательный 	Адрес компании. Внимание! При передаче текстовой части адреса автоматическая подстановка координат адреса (геокодинг) не осуществляется. Для того, чтобы адрес отображался на карте, необходимо дополнительно передать координаты адреса в параметре coordinates. Перевести текстовую часть адреса в координаты можно с помощью сервисов геокодинга, например DaData.ru, Google Geocoding API и т.д.
    coordinates         	list[float] 	    необязательный 	Координаты компании
    comment 	            string 	            необязательный 	Дополнительная информация о компании
    observer_ids        	list[int]        	необязательный 	Массив из ID пользователей, являющихся наблюдателями компании
    default_assignee_id 	integer 	        необязательный 	ID сотрудника, назначенного ответственным по умолчанию для этой компании
    category_code       	string 	            необязательный 	Код категории клиента
    crm_1c_id 	            string 	            необязательный 	Идентификатор объекта в 1С. Необходим для интеграции с 1С, не отображается в web-интерфейсе
    custom_parameters 	    associative array 	опционально 	Дополнительные атрибуты компании"""

    def __init__(
        self,
        name: str,
        additional_name: typing.Optional[str] = None,
        site: typing.Optional[str] = None,
        email: typing.Optional[str] = None,
        phone: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        coordinates: typing.Optional[list] = None,
        comment: typing.Optional[str] = None,
        observer_ids: typing.Optional[list] = None,
        default_assignee_id: typing.Optional[int] = None,
        category_code: typing.Optional[str] = None,
        crm_1c_id: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
    ):
        """

        :param name: Company name (Название компании)
        :param additional_name:  Additional company name (Дополнительное название компании)
        :param site:  Company website (Сайт компании)
        :param email: Company E-mail (Контактный E-mail компании)
        :param phone: Company phone (Контактный телефон компании)
        :param address: Company address (Адрес компании)
        :param coordinates: Company coordinates (Координаты компании)
        :param comment: Additional information about the company (Дополнительная информация о компании)
        :param observer_ids: Array of user IDs who are observers of the company (Массив из ID пользователей, являющихся наблюдателями компании)`
        :param default_assignee_id: Employee ID assigned as the default responsible for this company (ID сотрудника, назначенного ответственным по умолчанию для этой компании)
        :param category_code: Customer category code (Код категории клиента)
        :param crm_1c_id: Object identifier in 1C (Идентификатор объекта в 1С). Required for integration with 1C, not displayed in the web interface
        :param custom_parameters: Additional company attributes (Дополнительные атрибуты компании)
        """
        self.name: str = name
        self.additional_name: typing.Optional[str] = additional_name
        self.site: typing.Optional[str] = site
        self.email: typing.Optional[str] = email
        self.phone: typing.Optional[str] = phone
        self.address: typing.Optional[str] = address
        self.coordinates: typing.Optional[list] = coordinates
        self.comment: typing.Optional[str] = comment
        self.observer_ids: typing.Optional[list] = observer_ids
        self.default_assignee_id: typing.Optional[int] = default_assignee_id
        self.category_code: typing.Optional[str] = category_code
        self.crm_1c_id: typing.Optional[str] = crm_1c_id
        self.custom_parameters: typing.Optional[dict] = custom_parameters

    def to_request(self) -> dict:
        json_data = {
            "name": self.name,
        }
        if self.additional_name is not None:
            json_data["additional_name"] = self.additional_name
        if self.site is not None:
            json_data["site"] = self.site
        if self.email is not None:
            json_data["email"] = self.email
        if self.phone is not None:
            json_data["phone"] = self.phone
        if self.address is not None:
            json_data["address"] = self.address
        if self.coordinates is not None:
            json_data["coordinates"] = self.coordinates
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.observer_ids is not None:
            json_data["observer_ids"] = self.observer_ids
        if self.default_assignee_id is not None:
            json_data["default_assignee_id"] = self.default_assignee_id
        if self.category_code is not None:
            json_data["category_code"] = self.category_code
        if self.crm_1c_id is not None:
            json_data["crm_1c_id"] = self.crm_1c_id
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        return {
            "method": "POST",
            "url": "api/v1/companies/",
            "json": {"company": json_data},
        }

    def from_response(self, response: dict) -> Company:
        return Company.json_parse(response)


class UpdateCompanyRequest(types.ApiRequest):
    """Редактирование компании
    https://okdesk.ru/apidoc#!kompanii-redaktirovanie-kompanii

    PATCH /api/v1/companies/{company_id}

    Допустимые параметры запроса: ¶
    Название 	            Тип 	            Обязательность 	Описание
    name 	                string 	            необязательный 	Название компании
    additional_name 	    string 	            необязательный 	Дополнительное название компании
    site 	                string 	            необязательный 	Сайт компании
    email 	                string 	            необязательный 	Контактный E-mail компании
    phone 	                string 	            необязательный 	Контактный телефон компании
    address         	    string 	            необязательный 	Адрес компании. Внимание! При передаче текстовой части адреса автоматическая подстановка координат адреса (геокодинг) не осуществляется. Для того, чтобы адрес отображался на карте, необходимо дополнительно передать координаты адреса в параметре coordinates. Перевести текстовую часть адреса в координаты можно с помощью сервисов геокодинга, например DaData.ru, Google Geocoding API и т.д.
    coordinates         	list[float] 	    необязательный 	Координаты компании
    comment 	            string 	            необязательный 	Дополнительная информация о компании
    observer_ids        	list[int]        	необязательный 	Массив из ID пользователей, являющихся наблюдателями компании
    default_assignee_id 	integer 	        необязательный 	ID сотрудника, назначенного ответственным по умолчанию для этой компании
    category_code       	string 	            необязательный 	Код категории клиента
    crm_1c_id 	            string 	            необязательный 	Идентификатор объекта в 1С. Необходим для интеграции с 1С, не отображается в web-интерфейсе
    custom_parameters 	    associative array 	опционально 	Дополнительные атрибуты компании"""

    def __init__(
        self,
        company_id: int,
        name: typing.Optional[str] = None,
        additional_name: typing.Optional[str] = None,
        site: typing.Optional[str] = None,
        email: typing.Optional[str] = None,
        phone: typing.Optional[str] = None,
        address: typing.Optional[str] = None,
        coordinates: typing.Optional[list] = None,
        comment: typing.Optional[str] = None,
        observer_ids: typing.Optional[list] = None,
        default_assignee_id: typing.Optional[int] = None,
        category_code: typing.Optional[str] = None,
        crm_1c_id: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
    ):
        """

        :param company_id: Company ID to update (ID компании, которую нужно обновить)
        :param name: Company name (Название компании)
        :param additional_name:  Additional company name (Дополнительное название компании)
        :param site:  Company website (Сайт компании)
        :param email: Company E-mail (Контактный E-mail компании)
        :param phone: Company phone (Контактный телефон компании)
        :param address: Company address (Адрес компании)
        :param coordinates: Company coordinates (Координаты компании)
        :param comment: Additional information about the company (Дополнительная информация о компании)
        :param observer_ids: Array of user IDs who are observers of the company (Массив из ID пользователей, являющихся наблюдателями компании)`
        :param default_assignee_id: Employee ID assigned as the default responsible for this company (ID сотрудника, назначенного ответственным по умолчанию для этой компании)
        :param category_code: Customer category code (Код категории клиента)
        :param crm_1c_id: Object identifier in 1C (Идентификатор объекта в 1С). Required for integration with 1C, not displayed in the web interface
        :param custom_parameters: Additional company attributes (Дополнительные атрибуты компании)
        """
        self.company_id = company_id
        self.name: str = name
        self.additional_name: typing.Optional[str] = additional_name
        self.site: typing.Optional[str] = site
        self.email: typing.Optional[str] = email
        self.phone: typing.Optional[str] = phone
        self.address: typing.Optional[str] = address
        self.coordinates: typing.Optional[list] = coordinates
        self.comment: typing.Optional[str] = comment
        self.observer_ids: typing.Optional[list] = observer_ids
        self.default_assignee_id: typing.Optional[int] = default_assignee_id
        self.category_code: typing.Optional[str] = category_code
        self.crm_1c_id: typing.Optional[str] = crm_1c_id
        self.custom_parameters: typing.Optional[dict] = custom_parameters

    def to_request(self) -> dict:
        json_data = {}
        if self.name is not None:
            json_data["name"] = self.name
        if self.additional_name is not None:
            json_data["additional_name"] = self.additional_name
        if self.site is not None:
            json_data["site"] = self.site
        if self.email is not None:
            json_data["email"] = self.email
        if self.phone is not None:
            json_data["phone"] = self.phone
        if self.address is not None:
            json_data["address"] = self.address
        if self.coordinates is not None:
            json_data["coordinates"] = self.coordinates
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.observer_ids is not None:
            json_data["observer_ids"] = self.observer_ids
        if self.default_assignee_id is not None:
            json_data["default_assignee_id"] = self.default_assignee_id
        if self.category_code is not None:
            json_data["category_code"] = self.category_code
        if self.crm_1c_id is not None:
            json_data["crm_1c_id"] = self.crm_1c_id
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        return {
            "method": "POST",
            "url": "api/v1/companies/" + str(self.company_id),
            "json": {"company": json_data},
        }

    def from_response(self, response: dict) -> Company:
        return Company.json_parse(response)


class GetCompanyListRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-polucheniya-spiska-kompanij-po-parametram-poluchenie-spiska-po-parametram
    GET /api/v1/companies/list

    Допустимые параметры запроса:
    Название 	                Тип 	            Обязательность 	Описание

    category_ids 	            array of integer 	опционально 	Массив из ID категорий компаний (для отображения компаний без категорий необходимо передавать в параметре значение “0”).
    Пример: category_ids[]=1

    default_assignee_ids 	    array of integer 	опционально 	Массив из ID сотрудников, которые являются ответственными за компании (для отображения компаний без ответственного необходимо передавать в параметре значение “0”).
    Пример: default_assignee_ids[]=1

    default_assignee_group_ids 	array of integer 	опционально 	Массив из ID ответственных групп компаний (для отображения компаний без ответственной группы необходимо передавать в параметре значение “0”).
    Пример: default_assignee_group_ids[]=1

    observer_ids 	            array of integer 	опционально 	Массив из ID сотрудников, которые являются наблюдателями компаний (для отображения компаний без наблюдателей необходимо передавать в параметре значение “0”).
    Пример: observer_ids[]=1

    observer_group_ids 	        array of integer 	опционально 	Массив из ID групп наблюдателей компаний (для отображения компаний без групп наблюдателей необходимо передавать в параметре значение “0”).
    Пример: observer_group_ids[]=1

    created_since 	            string 	            опционально 	Дата создания компании в часовом поясе аккаунта (С)
    Пример: created_since=2019-05-25

    created_until 	            string 	            опционально 	Дата создания компании в часовом поясе аккаунта (По)
    Пример: created_until=2019-05-25

    custom_parameters 	        associative array 	опционально 	Ассоциативный массив из пар Код дополнительного атрибута: Значение или набор значений

    name 	                    string 	            опционально 	Название компании
    Пример: name=Okdesk

    additional_name 	        string 	            опционально 	Дополнительное название компании
    Пример: additional_name=Help Desk система для сервисных компаний

    crm_1c_id 	                string 	            опционально 	Идентификатор объекта в 1С
    Пример: crm_1c_id=35067c4b23a8

    page 	                    associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка компаний (подробное описание представлено в таблице ниже).


    =================================
    Допустимые параметры постраничного вывода:

    Название 	Тип значения 	Обязательность 	Описание
    size 	    integer 	    опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	    опционально 	ID компании, с которой начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id компании.
    Пример: page[from_id]=10

    direction 	string 	        опционально 	Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id компании.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id компании.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        category_ids: typing.List[int] = None,
        default_assignee_ids: typing.List[int] = None,
        default_assignee_group_ids: typing.List[int] = None,
        observer_ids: typing.List[int] = None,
        observer_group_ids: typing.List[int] = None,
        created_since: datetime.date = None,
        created_until: datetime.date = None,
        custom_parameters: typing.List[helpers.AttributeFilter] = None,
        name: str = None,
        additional_name: str = None,
        crm_1c_id: str = None,
        page_size: int = None,
        page_from_id: int = None,
        page_direction: typing.Literal["reverse", "forward"] = None,
    ):
        """

        :param category_ids: Category ids of companies (ID категорий компаний)
        :param default_assignee_ids: Default assignee ids of companies (ID исполнителей по умолчанию)
        :param default_assignee_group_ids: Default assignee group ids of companies (ID групп исполнителей по умолчанию)
        :param observer_ids: Observer ids of companies (ID наблюдателей)
        :param observer_group_ids: Observer group ids of companies (ID групп наблюдателей)
        :param created_since: Created since (Дата создания с)
        :param created_until: Created until (Дата создания по)
        :param custom_parameters: Custom parameters of companies (Параметры компаний)
        :param name: Name of companies (Название компаний)
        :param additional_name: Additional name of companies (Дополнительное название компаний)
        :param crm_1c_id: 1C id of companies (1C ID компаний)
        :param page_size: Number of returned records. Cannot exceed 100. (Число возвращаемых записей. Не может превышать 100.)
        :param page_from_id: ID of companies from which the selection of records begins. By default (if the direction parameter is not set) the selection is made in the direction from the value of from_id towards the decrease of the company id. (ID компаний, с которой начинается выборка записей. По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id компании.)
        :param page_direction: Direction of selection. Two values are available: reverse, forward. reverse - returns records whose ID is less than the value of from_id, if the from_id parameter is passed. If the from_id parameter is not passed, the selection is made from the largest company id value. forward - returns records whose ID is greater than the value of from_id, if the from_id parameter is passed. If the from_id parameter is not passed, the selection is made from the smallest company id value. (Направление выборки. Доступно два значения: reverse, forward. reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшего значения id компании. forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id компании.)
        """
        self.category_ids: typing.List[int] = category_ids
        self.default_assignee_ids: typing.List[int] = default_assignee_ids
        self.default_assignee_group_ids: typing.List[int] = default_assignee_group_ids
        self.observer_ids: typing.List[int] = observer_ids
        self.observer_group_ids: typing.List[int] = observer_group_ids
        self.created_since: datetime.date = created_since
        self.created_until: datetime.date = created_until
        self.custom_parameters: typing.List[helpers.AttributeFilter] = custom_parameters
        self.name: str = name
        self.additional_name: str = additional_name
        self.crm_1c_id: str = crm_1c_id

        self.page_size: int = page_size
        self.page_from_id: int = page_from_id
        self.page_direction: typing.Literal["reverse", "forward"] = page_direction

    def to_request(self) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}

        if self.category_ids:
            params["category_ids[]"] = [
                str(category_id) for category_id in self.category_ids
            ]
        if self.default_assignee_ids:
            params["default_assignee_ids[]"] = [
                str(default_assignee_id)
                for default_assignee_id in self.default_assignee_ids
            ]
        if self.default_assignee_group_ids:
            params["default_assignee_group_ids[]"] = [
                str(default_assignee_group_id)
                for default_assignee_group_id in self.default_assignee_group_ids
            ]
        if self.observer_ids:
            params["observer_ids[]"] = [
                str(observer_id) for observer_id in self.observer_ids
            ]
        if self.observer_group_ids:
            params["observer_group_ids[]"] = [
                str(observer_group_id) for observer_group_id in self.observer_group_ids
            ]
        if self.created_since:
            params["created_since"] = self.created_since.strftime("%Y-%m-%d")
        if self.created_until:
            params["created_until"] = self.created_until.strftime("%Y-%m-%d")
        if self.custom_parameters:
            params.update(
                helpers.convert_additional_attributes_filter(
                    "custom_parameters", self.custom_parameters
                )
            )
        if self.name:
            params["name"] = self.name
        if self.additional_name:
            params["additional_name"] = self.additional_name
        if self.crm_1c_id:
            params["crm_1c_id"] = self.crm_1c_id

        if self.page_size:
            params["page[size]"] = str(self.page_size)
        if self.page_from_id:
            params["page[from_id]"] = str(self.page_from_id)
        if self.page_direction:
            params["page[direction]"] = self.page_direction

        return {"method": "GET", "url": "api/v1/companies/list", "params": params}

    def from_response(self, response: dict) -> typing.List[Company]:
        return [Company.json_parse(x) for x in response]


class GetCompanyFileRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-fajla-kompanii-poluchenie-fajla-kompanii


    Получение файла компании
    GET /api/v1/companies/{company_id}/attachments/{attachment_id}

    company_id      integer    ID компании
    attachment_id   integer    ID вложения
    """

    def __init__(self, company_id: int, attachment_id: int):
        """

        :param company_id: Company ID (ID компании)
        :param attachment_id:  Attachment ID (ID вложения)
        """
        self.company_id: int = company_id
        self.attachment_id: int = attachment_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/companies/{self.company_id}/attachments/{self.attachment_id}",
        }

    def from_response(self, response: dict) -> shared.Attachment:
        return shared.Attachment.json_parse(response)


class ArchiveCompanyRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-arhivacziya-kompanii-arhivacziya-kompanii

    Архивация компании
    PATCH /api/v1/companies/{id}/activations
    """

    def __init__(self, company_id: int):
        """

        :param company_id: Company ID (ID компании)
        """
        self.company_id: int = company_id

    def to_request(self) -> dict:
        return {
            "method": "PATCH",
            "url": f"api/v1/companies/{self.company_id}/activations",
        }

    def from_response(self, response: dict) -> Company:
        return Company.json_parse(response)
