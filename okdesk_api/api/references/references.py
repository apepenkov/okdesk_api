import datetime
import typing

from ... import helpers
from ... import types


class EquipmentManufacturer(types.OkDeskBaseClass):
    """
    {
        "id": 5,
        "code": "005",
        "name": "manufacturer 5",
        "description": "somewhat special manufacturer",
        "visible": true
      },
    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.description: str = None
        self.visible: bool = None

    @classmethod
    def json_parse(cls, data: dict) -> "EquipmentManufacturer":
        instance = cls()
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.description = data.get("description")
        instance.visible = data.get("visible")
        return instance


class GetManufacturersRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-proizvoditelej-oborudovaniya-poluchenie-spiska-proizvoditelej-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	Тип 	Обязательность 	Описание
    search_string 	string 	опционально 	Искомая подстрока в названии или коде производителя оборудования

    page 	associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка производителей оборудования (подробное описание представлено в таблице ниже).

    Допустимые параметры постраничного вывода: ¶
    Название 	Тип значения 	Обязательность 	Описание
    size 	integer 	опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	опционально 	ID производителя оборудования, с которого начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id производителя.
    Пример: page[from_id]=10

    direction 	string 	опционально 	Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id производителя.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id производителя.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param search_string: String with search query (Строка с поисковым запросом)
        :param page_size: Number of returned records. Cannot exceed 100. (Количество возвращаемых записей. Не может превышать 100.)
        :param page_from_id: ID of the manufacturer of the equipment from which the selection of records begins. (ID производителя оборудования, с которого начинается выборка записей.)
        :param page_direction: Selection direction. (Направление выборки.)
        """
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
            "url": "api/v1/equipments/manufacturers/",
            "params": params,
        }

    def from_response(self, result) -> typing.List[EquipmentManufacturer]:
        return [EquipmentManufacturer.json_parse(x) for x in result]


class CreateManufacturerRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-proizvoditelej-oborudovaniya-sozdanie-proizvoditelya-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	    Тип 	Обязательность 	Описание
    name 	        string 	обязательный 	Название производителя оборудования
    code 	        string 	обязательный 	Код производителя оборудования
    description 	string 	необязательный 	Описание производителя оборудования
    """

    def __init__(
        self,
        name: str,
        code: str,
        description: typing.Optional[str] = None,
    ):
        """

        :param name: Name of the manufacturer of the equipment (Название производителя оборудования)
        :param code: Manufacturer code (Код производителя оборудования)
        :param description: Manufacturer description (Описание производителя оборудования)
        """
        self.name = name
        self.code = code
        self.description = description

    def to_request(self) -> dict:
        json_data = {
            "name": self.name,
            "code": self.code,
        }
        if self.description is not None:
            json_data["description"] = self.description
        return {
            "method": "POST",
            "url": "api/v1/equipments/manufacturers/",
            "json": {"equipment_manufacturer": json_data},
        }

    def from_response(self, result) -> EquipmentManufacturer:
        return EquipmentManufacturer.json_parse(result)


class EquipmentModel(types.OkDeskBaseClass):
    """
    {
        "id": 5,
        "code": "005",
        "name": "somewhatspecialequipment",
        "description": "somewhat special equipment",
        "visible": true,
        "equipment_kind": {
          "code": "002",
          "id": 2,
          "name": "sample_kind"
        },
        "equipment_manufacturer": {
          "code": "001",
          "id": 1,
          "name": "sample_manufacturer"
        }
      }
    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.description: str = None
        self.visible: bool = None
        self.equipment_kind: typing.Optional[types.CodeIdNamePair] = None
        self.equipment_manufacturer: typing.Optional[types.CodeIdNamePair] = None

    @classmethod
    def json_parse(cls, json_data) -> "EquipmentModel":
        result = cls()
        result.id = json_data.get("id")
        result.code = json_data.get("code")
        result.name = json_data.get("name")
        result.description = json_data.get("description")
        result.visible = json_data.get("visible")
        result.equipment_kind = json_data.get("equipment_kind")
        result.equipment_manufacturer = json_data.get("equipment_manufacturer")
        return result


class GetEquipmentModelsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-modelej-oborudovaniya-poluchenie-spiska-modelej-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	Тип 	Обязательность 	Описание
    search_string 	string 	опционально 	Искомая подстрока в названии или коде модели оборудования

    page 	associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка моделей оборудования (подробное описание представлено в таблице ниже).

    Допустимые параметры постраничного вывода: ¶
    Название 	Тип значения 	Обязательность 	Описание
    size 	integer 	опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30

    from_id 	integer 	опционально 	ID модели оборудования, с которого начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id модели.
    Пример: page[from_id]=10

    direction 	string 	опционально 	Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id модели.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id модели.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param search_string: Search string (Искомая подстрока в названии или коде модели оборудования)
        :param page_size: Page size (Число возвращаемых записей. Не может превышать 100.)
        :param page_from_id: Page from id (ID модели оборудования, с которого начинается выборка записей. По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id модели.)
        :param page_direction: Page direction (Направление выборки. Доступно два значения: reverse, forward. reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшего значения id модели. forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id модели.)
        """

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
            "url": "api/v1/equipments/models/",
            "params": params,
        }

    def from_response(self, result) -> typing.List[EquipmentModel]:
        return [EquipmentModel.json_parse(x) for x in result]


class CreateEquipmentModelRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-modelej-oborudovaniya-sozdanie-modelej-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	                Тип 	Обязательность 	Описание
    name 	                    string 	обязательный 	Название модели оборудования
    code 	                    string 	обязательный 	Код модели оборудования
    equipment_kind_id 	        integer обязательный 	ID типа оборудования
    equipment_manufacturer_id 	integer обязательный 	ID производителя оборудования
    description 	            string 	необязательный 	Описание модели оборудования
    """

    def __init__(
        self,
        name: str,
        code: str,
        equipment_kind_id: int,
        equipment_manufacturer_id: int,
        description: typing.Optional[str] = None,
    ):
        """

        :param name: Name (Название модели оборудования)
        :param code: Code (Код модели оборудования)
        :param equipment_kind_id: Equipment kind id (ID типа оборудования)
        :param equipment_manufacturer_id: Equipment manufacturer id (ID производителя оборудования)
        :param description: Description (Описание модели оборудования)
        """

        self.name = name
        self.code = code
        self.equipment_kind_id = equipment_kind_id
        self.equipment_manufacturer_id = equipment_manufacturer_id
        self.description = description

    def to_request(self) -> dict:
        json_data = {
            "name": self.name,
            "code": self.code,
            "equipment_kind_id": self.equipment_kind_id,
            "equipment_manufacturer_id": self.equipment_manufacturer_id,
        }
        if self.description is not None:
            json_data["description"] = self.description
        return {
            "method": "POST",
            "url": "api/v1/equipments/models/",
            "json": {"equipment_model": json_data},
        }

    def from_response(self, result) -> EquipmentModel:
        return EquipmentModel.json_parse(result)


class EquipmentKind(types.OkDeskBaseClass):
    """
    {
        "id": 5,
        "code": "005",
        "name": "somewhatspecialequipment",
        "description": "somewhat special equipment",
        "visible": true,
        "parameters": [
          {
            "name": "Some_parameter 3",
            "field_type": "ftcheckbox"
          }
        ]
    }
    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.description: str = None
        self.visible: bool = None
        self.parameters: typing.List[dict] = None

    @classmethod
    def json_parse(cls, json_data: dict) -> "EquipmentKind":
        instance = cls()
        instance.id = json_data.get("id")
        instance.code = json_data.get("code")
        instance.name = json_data.get("name")
        instance.description = json_data.get("description")
        instance.visible = json_data.get("visible")
        instance.parameters = json_data.get("parameters")
        return instance


class GetEquipmentKindsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-tipov-oborudovaniya-poluchenie-spiska-tipov-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	        Тип 	Обязательность 	Описание
    search_string 	    string 	необязательный 	Строка поиска
    page[size] 	        integer необязательный 	Количество элементов на странице
    page[from_id] 	    integer необязательный 	ID элемента, с которого начинать выборку
    page[direction] 	string 	необязательный 	Направление выборки ("reverse", "forward")
    """

    def __init__(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param search_string: Search string (Строка поиска)
        :param page_size: Page size (Количество элементов на странице)
        :param page_from_id: Page from id (ID элемента, с которого начинать выборку)
        :param page_direction: Page direction (Направление выборки ("reverse", "forward"))
        """

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
            "url": "api/v1/equipments/kinds/",
            "params": params,
        }

    def from_response(self, result) -> typing.List[EquipmentKind]:
        return [EquipmentKind.json_parse(x) for x in result]


class CreateEquipmentKindRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-tipov-oborudovaniya-sozdanie-tipa-oborudovaniya

    Допустимые параметры запроса: ¶
    Название 	        Тип 	            Обязательность 	Описание
    name 	            string 	            обязательный 	Название типа оборудования
    code 	            string 	            обязательный 	Код типа оборудования
    description 	    string 	            необязательный 	Описание типа оборудования
    parameter_codes 	array of string 	необязательный 	Массив из кодов связанных допополнительных атрибутов оборудования
    """

    def __init__(
        self,
        name: str,
        code: str,
        description: typing.Optional[str] = None,
        parameter_codes: typing.Optional[typing.List[str]] = None,
    ):
        """

        :param name: Name (Название типа оборудования)
        :param code: Code (Код типа оборудования)
        :param description: Description (Описание типа оборудования)
        :param parameter_codes: Parameter codes (Массив из кодов связанных допополнительных атрибутов оборудования)
        """

        self.name = name
        self.code = code
        self.description = description
        self.parameter_codes = parameter_codes

    def to_request(self) -> dict:
        json_data = {
            "name": self.name,
            "code": self.code,
        }
        if self.description is not None:
            json_data["description"] = self.description
        if self.parameter_codes is not None:
            json_data["parameter_codes"] = self.parameter_codes
        return {
            "method": "POST",
            "url": "api/v1/equipments/kinds/",
            "json": {"equipment_kind": json_data},
        }

    def from_response(self, result) -> EquipmentKind:
        return EquipmentKind.json_parse(result)
