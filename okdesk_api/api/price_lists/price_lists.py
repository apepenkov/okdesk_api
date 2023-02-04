import datetime
import typing

from ... import helpers
from ... import types


class PriceList(types.OkDeskBaseClass):
    """
    {
       "id": 101,
       "name": "Прайс-лист на обслуживание",
       "allow_without_category": false,
       "allow_without_company": false,
       "company_category_codes": [
         "partner",
         "client",
         "vipclient"
       ],
       "company_ids": [
         441,
         41
       ]
     },
     {
       "id": 100,
       "name": "Прайс-лист на услуги и продукты для всех клиентов",
       "allow_without_category": false,
       "allow_without_company": false,
       "company_category_codes": [],
       "company_ids": []
     }
    """

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.allow_without_category: bool = None
        self.allow_without_company: bool = None
        self.company_category_codes: typing.List[str] = None
        self.company_ids: typing.List[int] = None

    @classmethod
    def json_parse(cls, data: dict) -> "PriceList":
        instance = cls()
        instance.id = data.get("id")
        instance.name = data.get("name")
        instance.allow_without_category = data.get("allow_without_category")
        instance.allow_without_company = data.get("allow_without_company")
        instance.company_category_codes = data.get("company_category_codes")
        instance.company_ids = data.get("company_ids")
        return instance


class Service(types.OkDeskBaseClass):
    """
    {
      "id": 1,
      "code": "timerateservice",
      "name": "Услуги с повременной оплатой",
      "type": "service",
      "unit": "человеко-час",
      "price": 1000,
      "nds": 0,
      "visible": true,
      "description": "Различные биллингуемые услуги с почасовой оплатой"
    }
    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.type: str = None
        self.unit: str = None
        self.price: float = None
        self.nds: float = None
        self.visible: bool = None
        self.description: str = None

    @classmethod
    def json_parse(cls, data: dict) -> "Service":
        instance = cls()
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.type = data.get("type")
        instance.unit = data.get("unit")
        instance.price = data.get("price")
        instance.nds = data.get("nds")
        instance.visible = data.get("visible")
        instance.description = data.get("description")
        return instance


class ServiceWithPriceList(types.OkDeskBaseClass):
    """
    {
      "price_list_id": 3,
      "price_list_name": "Прайс-лист на обслуживание",
      "id": 1,
      "code": "timerateservice",
      "name": "Услуги с повременной оплатой",
      "type": "service",
      "unit": "человеко-час",
      "price": 1000,
      "nds": 0,
      "description": "Различные биллингуемые услуги с почасовой оплатой"
    }
    """

    def __init__(self):
        self.price_list_id: int = None
        self.price_list_name: str = None
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.type: str = None
        self.unit: str = None
        self.price: float = None
        self.nds: float = None
        self.description: str = None

    @classmethod
    def json_parse(cls, data: dict) -> "ServiceWithPriceList":
        instance = cls()
        instance.price_list_id = data.get("price_list_id")
        instance.price_list_name = data.get("price_list_name")
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.type = data.get("type")
        instance.unit = data.get("unit")
        instance.price = data.get("price")
        instance.nds = data.get("nds")
        instance.description = data.get("description")
        return instance


class GetPriceListListRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-polucheniya-spiska-prajs-listov-metod-polucheniya-spiska-prajs-listov

    GET /api/v1/price_lists

    Допустимые параметры постраничного вывода: ¶
    Название 	    Тип значения 	Обязательность 	Описание
    size 	        integer 	    опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	    integer 	    опционально 	ID строки справочника, с которой начинается выборка записей. По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id строки справочника.
    Пример: page[from_id]=10

    direction 	    string 	        опционально 	Направление выборки.     Доступно два значения: reverse, forward.

    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id строки справочника.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id строки справочника.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.size = size
        self.from_id = from_id
        self.direction = direction

    def to_request(self) -> dict:
        params = {}
        if self.size is not None:
            params["page[size]"] = self.size
        if self.from_id is not None:
            params["page[from_id]"] = self.from_id
        if self.direction is not None:
            params["page[direction]"] = self.direction

        return {
            "method": "GET",
            "url": "api/v1/price_lists",
            "params": params,
        }

    def from_response(self, result) -> typing.List[PriceList]:
        return [PriceList.json_parse(item) for item in result]


class GetPriceListServicesRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-polucheniya-prajs-lista-metod-polucheniya-prajs-lista

    GET /api/v1/price_lists/{price_list_id}/services

    Допустимые параметры запроса: ¶
    Название 	    Тип значения 	    Обязательность 	Описание
    types 	        array of string 	обязательный 	Массив разделов прайс-листа. Допустимые значения: service, work, product.
    Пример: &types[]=work&types[]=service

    size 	        integer 	    опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	    integer 	    опционально 	ID строки справочника, с которой начинается выборка записей. По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id строки справочника.
    Пример: page[from_id]=10

    direction 	    string 	        опционально 	Направление выборки.     Доступно два значения: reverse, forward.

    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id строки справочника.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id строки справочника.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        price_list_id: int,
        types_: typing.List[typing.Literal["service", "work", "product"]],
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.price_list_id = price_list_id
        self.types_ = types_
        self.size = size
        self.from_id = from_id
        self.direction = direction

    def to_request(self) -> dict:
        params = {"types": self.types_}
        if self.size is not None:
            params["page[size]"] = self.size
        if self.from_id is not None:
            params["page[from_id]"] = self.from_id
        if self.direction is not None:
            params["page[direction]"] = self.direction

        return {
            "method": "GET",
            "url": f"api/v1/price_lists/{self.price_list_id}/services",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Service]:
        return [Service.json_parse(item) for item in result]


class AddServiceToPriceListRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-dobavleniya-stroki-prajs-lista-metod-dobavleniya-stroki-prajs-lista

    POST /api/v1/price_lists/{price_list_id}/services

    Допустимые параметры запроса: ¶
    Название 	    Тип 	Обязательность 	Описание
    code 	        string 	обязательный 	Код строки справочника
    name 	        string 	обязательный 	Название строки справочника
    type 	        string 	обязательный 	Раздел строки справочника. Допустимые значения: work, product, service
    unit 	        string 	обязательный 	Единица измерения
    price 	        number 	обязательный 	Цена
    nds 	        integer обязательный 	Ставка НДС, %
    visible 	    boolean опционально 	Статус активности. Принимает значение true или false
    description 	string 	опционально 	Описание
    """

    def __init__(
        self,
        price_list_id: int,
        code: str,
        name: str,
        type_: typing.Literal["work", "product", "service"],
        unit: str,
        price: float,
        nds: int,
        visible: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
    ):
        self.price_list_id = price_list_id
        self.code = code
        self.name = name
        self.type_ = type_
        self.unit = unit
        self.price = price
        self.nds = nds
        self.visible = visible
        self.description = description

    def to_request(self) -> dict:
        json_data = {
            "code": self.code,
            "name": self.name,
            "type": self.type_,
            "unit": self.unit,
            "price": self.price,
            "nds": self.nds,
        }
        if self.visible is not None:
            json_data["visible"] = self.visible
        if self.description is not None:
            json_data["description"] = self.description

        return {
            "method": "POST",
            "url": f"api/v1/price_lists/{self.price_list_id}/services",
            "json": {"service": json_data},
        }

    def from_response(self, result) -> Service:
        return Service.json_parse(result)


class UpdateServiceInPriceListRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-redaktirovaniya-stroki-prajs-lista-metod-redaktirovaniya-stroki-prajs-lista

    PATCH /api/v1/price_lists/{price_list_id}/services/{code}

    Допустимые параметры запроса: ¶
    Название 	    Тип 	Обязательность 	Описание
    code 	        string 	опционально 	Код строки справочника
    name 	        string 	опционально 	Название строки справочника
    type 	        string 	опционально 	Раздел строки справочника. Допустимые значения: work, product, service
    unit 	        string 	опционально 	Единица измерения
    price 	        number 	опционально 	Цена
    nds 	        integer опционально 	Ставка НДС, %
    visible 	    boolean опционально 	Статус активности. Принимает значение true или false
    description 	string 	опционально 	Описание
    """

    def __init__(
        self,
        price_list_id: int,
        code: str,
        name: typing.Optional[str] = None,
        type_: typing.Optional[typing.Literal["work", "product", "service"]] = None,
        unit: typing.Optional[str] = None,
        price: typing.Optional[float] = None,
        nds: typing.Optional[int] = None,
        visible: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
    ):
        self.price_list_id = price_list_id
        self.code = code
        self.name = name
        self.type_ = type_
        self.unit = unit
        self.price = price
        self.nds = nds
        self.visible = visible
        self.description = description

    def to_request(self) -> dict:
        json_data = {}
        if self.name is not None:
            json_data["name"] = self.name
        if self.type_ is not None:
            json_data["type"] = self.type_
        if self.unit is not None:
            json_data["unit"] = self.unit
        if self.price is not None:
            json_data["price"] = self.price
        if self.nds is not None:
            json_data["nds"] = self.nds
        if self.visible is not None:
            json_data["visible"] = self.visible
        if self.description is not None:
            json_data["description"] = self.description

        return {
            "method": "PATCH",
            "url": f"api/v1/price_lists/{self.price_list_id}/services/{self.code}",
            "json": {"service": json_data},
        }

    def from_response(self, result) -> Service:
        return Service.json_parse(result)


class GetAvailableServicesForIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!metod-polucheniya-dostupnogo-nabora-strok-prajs-lista-dlya-zayavki-i-polzovatelya-metod-polucheniya-dostupnogo-nabora-strok-prajs-lista-dlya-zayavki-i-polzovatelya

    GET /api/v1/issues/{issue_id}/available_services

    Допустимые параметры запроса: ¶
    Название 	    Тип 	            Обязательность 	    Описание
    search_string 	string 	            опционально 	    Искомая подстрока в названии строки прайс-листа

    page 	        associative array 	опционально 	 	Ассоциативный массив параметров постраничного вывода прайс-листа (подробное описание представлено в таблице ниже).

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
        issue_id: int,
        search_string: str = None,
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        self.issue_id = issue_id
        self.search_string = search_string
        self.size = size
        self.from_id = from_id
        self.direction = direction

    def to_request(self) -> dict:
        params = {}
        if self.search_string is not None:
            params["search_string"] = self.search_string
        if self.size is not None:
            params["page[size]"] = self.size
        if self.from_id is not None:
            params["page[from_id]"] = self.from_id
        if self.direction is not None:
            params["page[direction]"] = self.direction
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/available_services",
            "params": params,
        }

    def from_response(self, result) -> typing.List[ServiceWithPriceList]:
        return [ServiceWithPriceList.json_parse(x) for x in result]
