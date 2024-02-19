import datetime
import typing

from ... import helpers
from ... import types


class Equipment(types.OkDeskBaseClass):
    """
    https://okdesk.ru/apidoc#!redaktirovanie-oborudovaniya-informacziya-ob-oborudovanii

    {
      "id": 3,
      "serial_number": "1101040003532",
      "inventory_number": "51BKB835225",
      "maintenance_entity_id": 15,
      "parent_id": 43,
      "equipment_kind": {
        "id": 24,
        "code": "laptop",
        "name": "Ноутбук",
        "description": ""
      },
      "equipment_manufacturer": null,
      "equipment_model": null,
      "company": {
        "id": 45,
        "name": "Интеллект+",
        "additional_name": null,
        "site": "intellectplus.com",
        "email": "intel+@okdesk.ru",
        "phone": "+8412 381312",
        "address": "Москва, Тверская-Ямская д.58",
        "comment": "",
        "attachments": [
          {
            "id": 8,
            "attachment_file_name": "photo.jpg",
            "description": "Фотография неисправности",
            "attachment_file_size": 4149,
            "is_public": false,
            "created_at": "2016-09-30T09:28:50.499+03:00"
          }
        ]
      },
      "parameters": [
        {
          "code": "end_of_service_period",
          "name": "Дата окончания сервисного периода",
          "field_type": "ftdate",
          "value": "2018-03-16"
        },
        {
          "code": "color",
          "name": "Цвет",
          "field_type": "ftstring",
          "value": "black"
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
        self.serial_number: str = None
        self.inventory_number: str = None
        self.comment: str = None
        self.company: dict = None
        self.maintenance_entity_id: int = None
        self.parent_id: int = None
        self.parameters: typing.List[dict] = []
        self.equipment_kind: dict = {}
        self.equipment_manufacturer: dict = {}
        self.equipment_model: dict = {}
        self.agreements: typing.List[dict] = []

    @classmethod
    def json_parse(cls, data: dict) -> "Equipment":
        instance = cls()
        instance.id = data.get("id")
        instance.serial_number = data.get("serial_number")
        instance.inventory_number = data.get("inventory_number")
        instance.comment = data.get("comment")
        instance.company = data.get("company")
        instance.maintenance_entity_id = data.get("maintenance_entity_id")
        instance.parent_id = data.get("parent_id")
        instance.parameters = data.get("parameters")
        instance.equipment_kind = data.get("equipment_kind")
        instance.equipment_manufacturer = data.get("equipment_manufacturer")
        instance.equipment_model = data.get("equipment_model")
        instance.agreements = data.get("agreements")
        return instance


class FindEquipmentRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!oborudovanie-poisk-oborudovaniya

    Параметры URI

    inventory_number        string (необязательное) Пример: 1101040003532     Инвентарный номер оборудования
    serial_number           string (необязательное) Пример: 51BKB835225       Серийный номер оборудования
    search_string           string (необязательное) Пример: desk              Искомая подстрока
    """

    def __init__(
        self,
        inventory_number: str = None,
        serial_number: str = None,
        search_string: str = None,
    ):
        """

        :param inventory_number: Inventory number of equipment (Инвентарный номер оборудования)
        :param serial_number: Serial number of equipment (Серийный номер оборудования)
        :param search_string: Search string (Искомая подстрока)
        """
        self.inventory_number = inventory_number
        self.serial_number = serial_number
        self.search_string = search_string

    def to_request(self) -> dict:
        params = {}
        if self.inventory_number:
            params["inventory_number"] = self.inventory_number
        if self.serial_number:
            params["serial_number"] = self.serial_number
        if self.search_string:
            params["search_string"] = self.search_string
        return {
            "method": "GET",
            "url": "api/v1/equipments",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Equipment]:
        # why does api return a single dict NOT within a list if only 0/1 items are found?
        if not result:
            return []
        return (
            [Equipment.json_parse(item) for item in result]
            if isinstance(result, list)
            else [Equipment.json_parse(result)]
        )


class CreateEquipmentRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!oborudovanie-sozdanie-oborudovaniya

    Название 	                    Тип 	            Обязательность 	Описание
    equipment_type_code 	        string 	            обязательный 	Код типа оборудования
    equipment_manufacturer_code 	string 	            опционально 	Код производителя оборудования
    equipment_model_code 	        string 	            опционально 	Код модели оборудования
    serial_number 	                string 	            опционально 	Серийный номер
    inventory_number 	            string 	            опционально 	Инвентарный номер
    comment 	                    string 	            опционально 	Комментарий
    company_id 	                    string 	            опционально 	ID компании, привязанной к оборудованию
    maintenance_entity_id 	        string 	            опционально 	ID объекта обслуживания, к которому привязано оборудование
    parent_id 	                    string 	            опционально 	ID головного оборудования
    custom_parameters 	            associative array 	опционально 	Дополнительные атрибуты оборудования
    agreement_ids 	                associative array 	опционально 	Набор ID договоров оборудования
    """

    def __init__(
        self,
        equipment_type_code: str,
        equipment_manufacturer_code: str = None,
        equipment_model_code: typing.Optional[str] = None,
        serial_number: typing.Optional[str] = None,
        inventory_number: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        company_id: typing.Optional[str] = None,
        maintenance_entity_id: typing.Optional[str] = None,
        parent_id: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
        agreement_ids: typing.Optional[typing.List[int]] = None,
    ):
        """

        :param equipment_type_code: Equipment type code (Код типа оборудования)
        :param equipment_manufacturer_code: Equipment manufacturer code (Код производителя оборудования)
        :param equipment_model_code: Equipment model code (Код модели оборудования)
        :param serial_number: Serial number (Серийный номер)
        :param inventory_number: Inventory number (Инвентарный номер)
        :param comment: Comment (Комментарий)
        :param company_id: Company ID (ID компании, привязанной к оборудованию)
        :param maintenance_entity_id: Maintenance entity ID (ID объекта обслуживания, к которому привязано оборудование)
        :param parent_id: Parent ID (ID головного оборудования)
        :param custom_parameters: Custom parameters (Дополнительные атрибуты оборудования)
        :param agreement_ids: Agreement IDs (Набор ID договоров оборудования)
        """
        self.equipment_type_code = equipment_type_code
        self.equipment_manufacturer_code = equipment_manufacturer_code
        self.equipment_model_code = equipment_model_code
        self.serial_number = serial_number
        self.inventory_number = inventory_number
        self.comment = comment
        self.company_id = company_id
        self.maintenance_entity_id = maintenance_entity_id
        self.parent_id = parent_id
        self.custom_parameters = custom_parameters
        self.agreement_ids = agreement_ids

    def to_request(self) -> dict:
        json_data = {
            "equipment_type_code": self.equipment_type_code,
        }
        if self.equipment_manufacturer_code is not None:
            json_data["equipment_manufacturer_code"] = self.equipment_manufacturer_code
        if self.equipment_model_code is not None:
            json_data["equipment_model_code"] = self.equipment_model_code
        if self.serial_number is not None:
            json_data["serial_number"] = self.serial_number
        if self.inventory_number is not None:
            json_data["inventory_number"] = self.inventory_number
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.company_id is not None:
            json_data["company_id"] = self.company_id
        if self.maintenance_entity_id is not None:
            json_data["maintenance_entity_id"] = self.maintenance_entity_id
        if self.parent_id is not None:
            json_data["parent_id"] = self.parent_id
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        if self.agreement_ids is not None:
            json_data["agreement_ids"] = self.agreement_ids
        return {
            "method": "POST",
            "url": "api/v1/equipments/",
            "json": {"equipment": json_data},
        }

    def from_response(self, result) -> Equipment:
        return Equipment.json_parse(result)


class UpdateEquipmentRequest(types.ApiRequest):
    """
    Обновление оборудования

    equipment_id 	                string 	            обязательно 	ID оборудования
    equipment_type_code 	        string 	            опционально 	Код типа оборудования
    equipment_manufacturer_code 	string 	            опционально 	Код производителя оборудования
    equipment_model_code 	        string 	            опционально 	Код модели оборудования
    serial_number 	                string 	            опционально 	Серийный номер
    inventory_number 	            string 	            опционально 	Инвентарный номер
    comment 	                    string 	            опционально 	Комментарий
    company_id 	                    string 	            опционально 	ID компании, привязанной к оборудованию
    maintenance_entity_id 	        string 	            опционально 	ID объекта обслуживания, к которому привязано оборудование
    parent_id 	                    string 	            опционально 	ID головного оборудования
    custom_parameters 	            associative array 	опционально 	Дополнительные атрибуты оборудования
    agreement_ids 	                associative array 	опционально 	Набор ID договоров оборудования
    """

    def __init__(
        self,
        equipment_id: int,
        equipment_type_code: typing.Optional[str] = None,
        equipment_manufacturer_code: typing.Optional[str] = None,
        equipment_model_code: typing.Optional[str] = None,
        serial_number: typing.Optional[str] = None,
        inventory_number: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        company_id: typing.Optional[str] = None,
        maintenance_entity_id: typing.Optional[str] = None,
        parent_id: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
        agreement_ids: typing.Optional[typing.List[int]] = None,
    ):
        """

        :param equipment_id: ID of equipment (ID оборудования)
        :param equipment_type_code: Equipment type code (Код типа оборудования)
        :param equipment_manufacturer_code: Equipment manufacturer code (Код производителя оборудования)
        :param equipment_model_code: Equipment model code (Код модели оборудования)
        :param serial_number: Serial number (Серийный номер)
        :param inventory_number: Inventory number (Инвентарный номер)
        :param comment: Comment (Комментарий)
        :param company_id: Company ID (ID компании, привязанной к оборудованию)
        :param maintenance_entity_id: Maintenance entity ID (ID объекта обслуживания, к которому привязано оборудование)
        :param parent_id: Parent ID (ID головного оборудования)
        :param custom_parameters: Custom parameters (Дополнительные атрибуты оборудования)
        :param agreement_ids: Agreement IDs (Набор ID договоров оборудования)
        """
        self.equipment_id = equipment_id
        self.equipment_type_code = equipment_type_code
        self.equipment_manufacturer_code = equipment_manufacturer_code
        self.equipment_model_code = equipment_model_code
        self.serial_number = serial_number
        self.inventory_number = inventory_number
        self.comment = comment
        self.company_id = company_id
        self.maintenance_entity_id = maintenance_entity_id
        self.parent_id = parent_id
        self.custom_parameters = custom_parameters
        self.agreement_ids = agreement_ids

    def to_request(self) -> dict:
        json_data = {}
        if self.equipment_type_code is not None:
            json_data["equipment_type_code"] = self.equipment_type_code
        if self.equipment_manufacturer_code is not None:
            json_data["equipment_manufacturer_code"] = self.equipment_manufacturer_code
        if self.equipment_model_code is not None:
            json_data["equipment_model_code"] = self.equipment_model_code
        if self.serial_number is not None:
            json_data["serial_number"] = self.serial_number
        if self.inventory_number is not None:
            json_data["inventory_number"] = self.inventory_number
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.company_id is not None:
            json_data["company_id"] = self.company_id
        if self.maintenance_entity_id is not None:
            json_data["maintenance_entity_id"] = self.maintenance_entity_id
        if self.parent_id is not None:
            json_data["parent_id"] = self.parent_id
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters
        if self.agreement_ids is not None:
            json_data["agreement_ids"] = self.agreement_ids
        return {
            "method": "PATCH",
            "url": f"api/v1/equipments/{self.equipment_id}",
            "json": json_data,
        }

    def from_response(self, result) -> Equipment:
        return Equipment.json_parse(result)


class GetEquipmentRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!redaktirovanie-oborudovaniya-informacziya-ob-oborudovanii
    Получение информации об оборудовании

    equipment_id 	string 	ID оборудования
    """

    def __init__(self, equipment_id: int):
        """

        :param equipment_id: ID of equipment (ID оборудования)
        """
        self.equipment_id = equipment_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/equipments/{self.equipment_id}",
        }

    def from_response(self, result) -> Equipment:
        return Equipment.json_parse(result)


class ListEquipmentsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-oborudovaniya-po-parametram-poluchenie-spiska-po-parametram

    Допустимые параметры запроса: ¶
    Название 	Тип 	Обязательность 	Описание
    company_ids 	array of integer 	опционально 	Массив из ID компаний (для отображения оборудования без компаний необходимо передавать в параметре значение “0”).
    Пример: company_ids[]=1

    maintenance_entity_ids 	array of integer 	опционально 	Массив из ID Объект обслуживания (для отображения оборудования без объектов обслуживания необходимо передавать в параметре значение “0”).
    Пример: maintenance_entity_ids[]=1

    agreement_ids 	array of integer 	опционально 	Массив из ID договоров (для отображения оборудования без договоров необходимо передавать в параметре значение “0”).
    Пример: agreement_ids[]=1

    created_since 	string 	опционально 	Дата создания оборудования в часовом поясе аккаунта (С)
    Пример: created_since=2019-05-25

    created_until 	string 	опционально 	Дата создания оборудования в часовом поясе аккаунта (По)
    Пример: created_until=2019-05-25

    equipment_kind_codes 	array of string 	опционально 	Массив из кодов типов оборудования.
    Пример: equipment_kind_codes[]=X

    equipment_manufacterer_codes 	array of string 	опционально 	Массив из кодов производителей оборудования.
    Пример: equipment_manufacturer_codes[]=X

    equipment_model_codes 	array of string 	опционально 	Массив из кодов моделей оборудования.
    Пример: equipment_model_codes[]=X

    custom_parameters 	associative array 	опционально 	Ассоциативный массив из пар Код дополнительного атрибута: Значение или набор значений

    page 	associative array 	опционально 	Ассоциативный массив параметров постраничного вывода списка оборудования (подробное описание представлено в таблице ниже).

    Допустимые параметры постраничного вывода:
    Название 	Тип значения 	Обязательность 	Описание
    size 	integer 	опционально 	Число возвращаемых записей. Не может превышать 100.
    Пример: page[size]=30
    from_id 	integer 	опционально 	ID оборудования, с которого начинается выборка записей.
    По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id оборудования.
    Пример: page[from_id]=10
    direction 	string 	опционально 	Направление выборки.
    Доступно два значения: reverse, forward.
    reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшого значения id оборудования.
    forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id оборудования.
    Пример: page[direction]=forward
    """

    def __init__(
        self,
        company_ids: typing.Optional[typing.List[int]] = None,
        maintenance_entity_ids: typing.Optional[typing.List[int]] = None,
        agreement_ids: typing.Optional[typing.List[int]] = None,
        created_since: typing.Optional[datetime.date] = None,
        created_until: typing.Optional[datetime.date] = None,
        equipment_kind_codes: typing.Optional[typing.List[str]] = None,
        equipment_manufacturer_codes: typing.Optional[typing.List[str]] = None,
        equipment_model_codes: typing.Optional[typing.List[str]] = None,
        custom_parameters: typing.Optional[typing.List[helpers.AttributeFilter]] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param company_ids: Array of company IDs (Массив ID компаний)
        :param maintenance_entity_ids: Array of maintenance entity IDs (Массив ID подразделений)
        :param agreement_ids: Array of agreement IDs (Массив ID договоров)
        :param created_since: Date of equipment creation from (Дата создания оборудования от)
        :param created_until: Date of equipment creation to (Дата создания оборудования до)
        :param equipment_kind_codes: Array of equipment kind codes (Массив кодов видов оборудования)
        :param equipment_manufacturer_codes: Array of equipment manufacturer codes (Массив кодов производителей оборудования)
        :param equipment_model_codes: Array of equipment model codes (Массив кодов моделей оборудования)
        :param custom_parameters: Custom parameters (Пользовательские параметры)
        :param page_size: Number of returned records (Число возвращаемых записей)
        :param page_from_id: ID of equipment from which the selection starts (ID оборудования, с которого начинается выборка записей)
        :param page_direction: Selection direction (Направление выборки)
        """
        self.company_ids = company_ids
        self.maintenance_entity_ids = maintenance_entity_ids
        self.agreement_ids = agreement_ids
        self.created_since = created_since
        self.created_until = created_until
        self.equipment_kind_codes = equipment_kind_codes
        self.equipment_manufacturer_codes = equipment_manufacturer_codes
        self.equipment_model_codes = equipment_model_codes
        self.custom_parameters = custom_parameters
        self.page_size = page_size
        self.page_from_id = page_from_id
        self.page_direction = page_direction

    def to_request(self) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.company_ids:
            params["company_ids[]"] = [
                str(company_id) for company_id in self.company_ids
            ]
        if self.maintenance_entity_ids:
            params["maintenance_entity_ids[]"] = [
                str(maintenance_entity_id)
                for maintenance_entity_id in self.maintenance_entity_ids
            ]
        if self.agreement_ids:
            params["agreement_ids[]"] = [
                str(agreement_id) for agreement_id in self.agreement_ids
            ]
        if self.created_since:
            params["created_since"] = self.created_since.strftime("%Y-%m-%d")
        if self.created_until:
            params["created_until"] = self.created_until.strftime("%Y-%m-%d")
        if self.equipment_kind_codes:
            params["equipment_kind_codes[]"] = self.equipment_kind_codes
        if self.equipment_manufacturer_codes:
            params["equipment_manufacturer_codes[]"] = self.equipment_manufacturer_codes
        if self.equipment_model_codes:
            params["equipment_model_codes[]"] = self.equipment_model_codes
        if self.custom_parameters:
            params.update(
                helpers.convert_additional_attributes_filter(
                    "custom_parameters", self.custom_parameters
                )
            )
        if self.page_size:
            params["page[size]"] = str(self.page_size)
        if self.page_from_id:
            params["page[from_id]"] = str(self.page_from_id)
        if self.page_direction:
            params["page[direction]"] = self.page_direction
        return {
            "method": "GET",
            "url": "api/v1/equipments/list/",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Equipment]:
        return [Equipment.json_parse(item) for item in result]
