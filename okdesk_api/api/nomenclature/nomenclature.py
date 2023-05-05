from ... import types
import datetime
import typing
from .. import shared
from ... import helpers


class Group(types.OkDeskBaseClass):
    """
    Example:

    {
        "id": 2058,
        "code": "test-group-1-1",
        "name": "test-group-1-1",
        "active": true,
        "group": {
            "id": 2057,
            "code": "test-group-1",
            "name": "test-group-1"
        }
    },
    {
        "id": 2057,
        "code": "test-group-1",
        "name": "test-group-1",
        "active": true,
        "group": null
    }

    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.active: bool = None
        # the following fields are parent group
        self.group_id: typing.Optional[int] = None
        self.group_code: typing.Optional[str] = None
        self.group_name: typing.Optional[str] = None

    @classmethod
    def json_parse(cls, data: dict) -> "Group":
        instance = cls()
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.active = data.get("active")
        group = data.get("group", None)
        if group:
            instance.group_id = group.get("id")
            instance.group_code = group.get("code")
            instance.group_name = group.get("name")
        return instance


class Position(types.OkDeskBaseClass):
    """
      Example:

      {
      "id": 101,
      "code": "item_code2",
      "name": "Услуги с повременной оплатой",
      "active": true,
      "item_type": "service",
      "unit": "человеко-час",
      "vendor_code": "",
      "description": "",
      "group": {
        "id": 100,
        "code": "group2",
        "name": "Родительская группа"
      }
    },
    {
      "id": 100,
      "code": "item_code1",
      "name": "Доставка в сервис",
      "active": true,
      "item_type": "work",
      "unit": "выезд",
      "vendor_code": "",
      "description": "",
      "group": null
    }

    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.active: bool = None
        self.item_type: str = None
        self.unit: str = None
        self.vendor_code: str = None
        self.description: str = None
        # the following fields are parent group
        self.group_id: typing.Optional[int] = None
        self.group_code: typing.Optional[str] = None
        self.group_name: typing.Optional[str] = None

    @classmethod
    def json_parse(cls, data: dict) -> "Position":
        instance = cls()
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.active = data.get("active")
        instance.item_type = data.get("item_type")
        instance.unit = data.get("unit")
        instance.vendor_code = data.get("vendor_code")
        instance.description = data.get("description")
        group = data.get("group", None)
        if group:
            instance.group_id = group.get("id")
            instance.group_code = group.get("code")
            instance.group_name = group.get("name")
        return instance


class GetGroupsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-grupp-nomenklatury-poluchenie-spiska-grupp-nomenklatury
    Допустимые параметры запроса: ¶
    Название 	    Тип 	            Обязательность 	Описание

    search_string 	string 	            опционально 	Искомая подстрока в названии группы номенклатуры
    code 	        string 	            опционально 	Строка фильтрации по коду группы номенклатуры
    page 	        associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка групп (подробное описание представлено в таблице ниже).


    Допустимые параметры постраничного вывода: ¶

    Название 	Тип значения Обязательность 	Описание

    size 	    integer 	опционально 	    Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	опционально 	    ID строки справочника, с которой начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id строки справочника.     Пример: page[from_id]=10

    direction 	string 	    опционально 	    Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id строки справочника.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id строки справочника.     Пример: page[direction]=forward

    """

    def __init__(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.search_string = search_string
        self.page_size = page_size
        self.page_from_id = page_from_id
        self.page_direction = page_direction

    def to_request(self) -> dict:
        params = {}
        if self.search_string is not None:
            params["search_string"] = self.search_string
        if self.page_size is not None:
            params["page[size]"] = self.page_size
        if self.page_from_id is not None:
            params["page[from_id]"] = self.page_from_id
        if self.page_direction is not None:
            params["page[direction]"] = self.page_direction
        return {
            "method": "GET",
            "url": "api/v1/nomenclature/groups",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Group]:
        return [Group.json_parse(x) for x in result]


class CreateGroupRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!dobavlenie-gruppy-nomenklatury-dobavlenie-gruppy-nomenklatury
    Допустимые параметры запроса: ¶
    Название 	Тип значения 	Обязательность 	Описание

    code 	    string 	        обязательно 	    Код группы номенклатуры
    name 	    string 	        обязательно 	    Название группы номенклатуры
    parent_id 	integer 	    опционально 	    ID родительской группы номенклатуры
    """

    def __init__(
        self,
        code: str,
        name: str,
        parent_id: typing.Optional[int] = None,
    ):
        self.code = code
        self.name = name
        self.parent_id = parent_id

    def to_request(self) -> dict:
        json_data = {
            "code": self.code,
            "name": self.name,
        }
        if self.parent_id is not None:
            json_data["parent_id"] = self.parent_id
        return {
            "method": "POST",
            "url": "api/v1/nomenclature/groups",
            "json": {"nomenclature_group": json_data},
        }

    def from_response(self, result) -> Group:
        return Group.json_parse(result)


class GetGroupRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-gruppy-nomenklatury-poluchenie-gruppy-nomenklatu
    Допустимые параметры запроса: ¶
    Название 	Тип значения 	Обязательность 	Описание

    id 	        integer 	    обязательно 	    ID группы номенклатуры
    """

    def __init__(
        self,
        group_id: int,
    ):
        self.id = group_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/nomenclature/groups/{self.id}",
        }

    def from_response(self, result) -> Group:
        return Group.json_parse(result)


class EditGroupRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-gruppy-nomenklatury-po-id-redaktirovaniya-gruppy-nomenklatury
    Допустимые параметры запроса: ¶
    Название 	Тип значения 	Обязательность 	Описание

    id 	        integer 	    обязательно 	    ID группы номенклатуры
    name 	    string 	        опционально 	    Название группы номенклатуры
    parent_id 	integer 	    опционально 	    ID родительской группы номенклатуры
    active 	    boolean 	    опционально 	    Статус активности. Принимает значение true или false
    """

    def __init__(
        self,
        group_id: int,
        name: typing.Optional[str] = None,
        parent_id: typing.Optional[int] = None,
        active: typing.Optional[bool] = None,
    ):
        self.id = group_id
        self.name = name
        self.parent_id = parent_id
        self.active = active

    def to_request(self) -> dict:
        json_data = {}
        if self.name is not None:
            json_data["name"] = self.name
        if self.parent_id is not None:
            json_data["parent_id"] = self.parent_id
        if self.active is not None:
            json_data["active"] = self.active
        return {
            "method": "PATCH",
            "url": f"api/v1/nomenclature/groups/{self.id}",
            "json": {"nomenclature_group": json_data},
        }

    def from_response(self, result) -> Group:
        return Group.json_parse(result)


class GetGroupPositionsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-poziczij-nomenklatury-poluchenie-spiska-poziczij-nomenklatury

    Допустимые параметры запроса: ¶
    Название 	    Тип 	            Обязательность 	Описание
    search_string 	string 	            опционально 	Искомая подстрока в названии, артикуле или описании позиции номенклатуры
    code 	        string 	            опционально 	Строка фильтрации по коду позиции номенклатуры
    item_types 	    array of string 	опционально 	Массив типов позиции номенклатуры. Допустимые значения: service, product, material, work. Пример: item_types[]=work&item_types[]=service
    group_id 	    integer 	        опционально 	ID группы для фильтрации по вхождению в группу (для отображения позиций номенклатуры без группы необходимо передавать в параметре значение “0”)
    page 	        associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка групп (подробное описание представлено в таблице ниже).

    Допустимые параметры постраничного вывода: ¶
    Название 	Тип значения 	Обязательность 	Описание
    size 	    integer 	опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	опционально 	ID строки справочника, с которой начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id строки справочника.
    Пример: page[from_id]=10

    direction 	string 	опционально 	Направление выборки.
    Доступно два значения: reverse, forward.

    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id строки справочника.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id строки справочника.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        search_string: typing.Optional[str] = None,
        code: typing.Optional[str] = None,
        item_types: typing.Optional[typing.List[str]] = None,
        group_id: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.search_string = search_string
        self.code = code
        self.item_types = item_types
        self.group_id = group_id
        self.page_size = page_size
        self.page_from_id = page_from_id
        self.page_direction = page_direction

    def to_request(self) -> dict:
        params = {}
        if self.search_string is not None:
            params["search_string"] = self.search_string
        if self.code is not None:
            params["code"] = self.code
        if self.item_types is not None:
            params["observer_ids[]"] = [str(x) for x in self.item_types]
        if self.group_id is not None:
            params["group_id"] = self.group_id
        if self.page_size is not None:
            params["page[size]"] = self.page_size
        if self.page_from_id is not None:
            params["page[from_id]"] = self.page_from_id
        if self.page_direction is not None:
            params["page[direction]"] = self.page_direction

        return {
            "method": "GET",
            "url": "api/v1/nomenclature/items",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Position]:
        return [Position.json_parse(x) for x in result]


class AddPositionRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!dobavlenie-poziczii-v-spravochnik-nomenklatury-dobavlenie-poziczii-v-spravochnik-nomenklatury

    Допустимые параметры запроса: ¶
    Название 	    Тип 	    Обязательность 	Описание
    code 	        string 	    обязательный 	Код позиции номенклатуры
    name 	        string 	    обязательный 	Название позиции номенклатуры
    item_type 	    string 	    обязательный 	Тип позиции номенклатуры. Допустимые значения: service, product, material, work
    unit 	        string 	    обязательный 	Единица измерения позиции номенклатуры
    description 	string 	    опционально 	Описание позиции номенклатуры
    group_id 	    integer 	опционально 	ID родительской группы
    vendor_code 	string 	    опционально 	Артикул позиции номенклатуры
    """

    def __init__(
        self,
        code: str,
        name: str,
        item_type: str,
        unit: str,
        description: typing.Optional[str] = None,
        group_id: typing.Optional[int] = None,
        vendor_code: typing.Optional[str] = None,
    ):
        self.code = code
        self.name = name
        self.item_type = item_type
        self.unit = unit
        self.description = description
        self.group_id = group_id
        self.vendor_code = vendor_code

    def to_request(self) -> dict:
        json_data = {
            "code": self.code,
            "name": self.name,
            "item_type": self.item_type,
            "unit": self.unit,
        }
        if self.description is not None:
            json_data["description"] = self.description
        if self.group_id is not None:
            json_data["group_id"] = self.group_id
        if self.vendor_code is not None:
            json_data["vendor_code"] = self.vendor_code

        return {
            "method": "POST",
            "url": "api/v1/nomenclature/items",
            "json": {"nomenclature_item": json_data},
        }

    def from_response(self, result) -> Position:
        return Position.json_parse(result)


class GetPositionRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-poziczii-nomenklatury-po-id-poluchenie-poziczii-nomenklatury-po-id

    Допустимые параметры запроса: ¶
    Название 	Тип значения 	Обязательность 	Описание
    id 	        integer 	    обязательный 	ID позиции номенклатуры
    """

    def __init__(self, position_id: int):
        self.id = position_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/nomenclature/items/{self.id}",
        }

    def from_response(self, result) -> Position:
        return Position.json_parse(result)


class EditNomenclaturePositionRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-poziczii-nomenklatury-po-id-redaktirovanie-poziczii-v-spravochnike-nomenklatury

    Допустимые параметры запроса: ¶
    Название 	    Тип 	    Обязательность 	Описание
    name 	        string 	    опционально 	Название позиции номенклатуры
    item_type 	    string 	    опционально 	Тип позиции номенклатуры. Допустимые значения: service, product, material, work
    unit 	        string 	    опционально 	Единица измерения позиции номенклатуры
    description 	string 	    опционально 	Описание позиции номенклатуры
    group_id 	    integer 	опционально 	ID родительской группы
    vendor_code 	string  	опционально 	Артикул позиции номенклатуры
    active 	        boolean 	опционально 	Статус активности. Принимает значение true или false
    """

    def __init__(
        self,
        position_id: int,
        name: typing.Optional[str] = None,
        item_type: typing.Optional[str] = None,
        unit: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        group_id: typing.Optional[int] = None,
        vendor_code: typing.Optional[str] = None,
        active: typing.Optional[bool] = None,
    ):
        self.id = position_id
        self.name = name
        self.item_type = item_type
        self.unit = unit
        self.description = description
        self.group_id = group_id
        self.vendor_code = vendor_code
        self.active = active

    def to_request(self) -> dict:
        json_data = {}
        if self.name is not None:
            json_data["name"] = self.name
        if self.item_type is not None:
            json_data["item_type"] = self.item_type
        if self.unit is not None:
            json_data["unit"] = self.unit
        if self.description is not None:
            json_data["description"] = self.description
        if self.group_id is not None:
            json_data["group_id"] = self.group_id
        if self.vendor_code is not None:
            json_data["vendor_code"] = self.vendor_code
        if self.active is not None:
            json_data["active"] = self.active

        return {
            "method": "PATCH",
            "url": f"api/v1/nomenclature/items/{self.id}",
            "json": {"nomenclature_item": json_data},
        }

    def from_response(self, result) -> Position:
        return Position.json_parse(result)


# the following classes and methods are new and connected to "nomencalture",
# but are still referenced to fron "price_list" in the API docs.
# however there's already old version of price_list implementation in the code, so the new one will be here.

# okdesk is weird.


class PriceListService(types.OkDeskBaseClass):
    """
    An element of price list.

      {
      "id": 1,
      "nomenclature_item_id": 1,
      "code": "timerateservice",
      "name": "Услуги с повременной оплатой",
      "type": "service",
      "group": {
        "id": 1,
        "code": "group_code",
        "name": "Услуги"
      },
      "unit": "человеко-час",
      "vendor_code": "",
      "price": 1000,
      "nds": 0,
      "visible": true,
      "description": "Различные биллингуемые услуги с почасовой оплатой"
    }
    """

    def __init__(self):
        self.id: int = None
        self.nomenclature_item_id: int = None
        self.code: str = None
        self.name: str = None
        self.type: str = None
        self.group: dict = None
        self.unit: str = None
        self.vendor_code: str = None
        self.price: int = None
        self.nds: int = None
        self.visible: bool = None
        self.description: str = None

    @classmethod
    def json_parse(cls, data: dict) -> "PriceListService":
        obj = cls()
        obj.id = data.get("id")
        obj.nomenclature_item_id = data.get("nomenclature_item_id")
        obj.code = data.get("code")
        obj.name = data.get("name")
        obj.type = data.get("type")
        obj.group = data.get("group")
        obj.unit = data.get("unit")
        obj.vendor_code = data.get("vendor_code")
        obj.price = data.get("price")
        obj.nds = data.get("nds")
        obj.visible = data.get("visible")
        obj.description = data.get("description")
        return obj


class GetPriceListServicesRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-prajs-lista-poluchenie-prajs-lista

    GET /api/v1/nomenclature/price_lists/{price_list_id}/services{?api_token}

    Допустимые параметры запроса: ¶
    Название 	    Тип 	            Обязательность 	Описание
    search_string 	string 	            опционально 	Искомая подстрока в названии элемента номенклатуры, артикуле или описании элемента номенклатуры.
    item_types 	    array of string 	опционально 	Массив строк для фильтрации по типу элемента номенклатуры. Допустимые значения: service, work, material, product.
    group_id 	    string 	            опционально 	ID группы в которую входит элемент номенклатуры (для отображения позиций номенклатуры без группы необходимо передавать в параметре значение “0”).
    page 	        associative array 	опционально 	Ассоциативный массив параметров постраничного вывода прайс-листа (подробное описание представлено в таблице ниже).

    Допустимые параметры постраничного вывода: ¶
    Название 	Тип значения 	Обязательность 	Описание
    size 	    integer 	    опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	    опционально 	ID строки справочника, с которой начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id строки справочника.
    Пример: page[from_id]=10

    direction 	string 	        опционально 	Направление выборки.
    Доступно два значения: reverse, forward.

    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id строки справочника.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id строки справочника.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        price_list_id: int,
        search_string: typing.Optional[str] = None,
        item_types: typing.Optional[list] = None,
        group_id: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.price_list_id = price_list_id
        self.search_string = search_string
        self.item_types = item_types
        self.group_id = group_id
        self.page_size = page_size
        self.page_from_id = page_from_id
        self.page_direction = page_direction

    def to_request(self) -> dict:
        params = {}
        if self.search_string is not None:
            params["search_string"] = self.search_string
        if self.item_types is not None:
            params["item_types"] = self.item_types
        if self.group_id is not None:
            params["group_id"] = self.group_id
        if self.page_size is not None:
            params["page[size]"] = self.page_size
        if self.page_from_id is not None:
            params["page[from_id]"] = self.page_from_id
        if self.page_direction is not None:
            params["page[direction]"] = self.page_direction

        return {
            "method": "GET",
            "url": f"api/v1/nomenclature/price_lists/{self.price_list_id}/services",
            "params": params,
        }

    def from_response(self, result) -> typing.List[PriceListService]:
        return [PriceListService.json_parse(item) for item in result]


class AddPriceListServiceRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-prajs-lista-dobavlenie-stroki-prajs-lista

    Допустимые параметры запроса: ¶
    Название 	            Тип 	        Обязательность 	Описание
    nomenclature_item_id 	integer 	    обязательный 	ID элемента справочника номенклатуры
    price 	                number      	обязательный 	Цена
    nds 	                integer 	    обязательный 	Ставка НДС, %
    """

    def __init__(
        self,
        price_list_id: int,
        nomenclature_item_id: int,
        price: float,
        nds: int,
    ):
        self.price_list_id = price_list_id
        self.nomenclature_item_id = nomenclature_item_id
        self.price = price
        self.nds = nds

    def to_request(self) -> dict:
        return {
            "method": "POST",
            "url": f"api/v1/nomenclature/price_lists/{self.price_list_id}/services",
            "json": {
                "service": {
                    "nomenclature_item_id": self.nomenclature_item_id,
                    "price": self.price,
                    "nds": self.nds,
                }
            },
        }

    def from_response(self, result) -> PriceListService:
        return PriceListService.json_parse(result)


class EditPriceListServiceRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-prajs-lista-redaktirovanie-stroki-prajs-lista

    Допустимые параметры запроса: ¶
    Название 	            Тип 	        Обязательность 	Описание
    price 	                number      	опционально 	Цена
    nds 	                integer 	    опционально 	Ставка НДС, %
    visible 	            boolean 	    опционально 	Статус активности. Принимает значение true или false
    """

    def __init__(
        self,
        price_list_id: int,
        service_id: int,
        price: typing.Optional[float] = None,
        nds: typing.Optional[int] = None,
        visible: typing.Optional[bool] = None,
    ):
        self.price_list_id = price_list_id
        self.service_id = service_id
        self.price = price
        self.nds = nds
        self.visible = visible

    def to_request(self) -> dict:
        json_data = {}
        if self.price is not None:
            json_data["price"] = self.price
        if self.nds is not None:
            json_data["nds"] = self.nds
        if self.visible is not None:
            json_data["visible"] = self.visible

        return {
            "method": "PUT",
            "url": f"api/v1/nomenclature/price_lists/{self.price_list_id}/services/{self.service_id}",
            "json": {"service": json_data},
        }

    def from_response(self, result) -> PriceListService:
        return PriceListService.json_parse(result)
