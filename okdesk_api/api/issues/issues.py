import os.path

import datetime
import typing
import mimetypes
from requests_toolbelt import MultipartEncoder
from ... import helpers
from ... import types
from .. import shared


class Comment(types.OkDeskBaseClass):
    """
    {
      "id": 1,
      "content": "В ближайшее время к Вам отправится инженер для решения проблемы.",
      "public": true,
      "attachments": [],
      "author": {
        "id": 10,
        "name": "Иванов Сергей Петрович",
        "type": "employee"
      }
    }
    """

    def __init__(self):
        self.id: int = None
        self.content: str = None
        self.public: bool = None
        self.attachments: typing.List[AddCommentRequest.Attachment] = None
        self.author: types.IdNameTypePair = None

    @classmethod
    def json_parse(cls, json_data: dict) -> "Comment":
        instance = cls()
        instance.id = json_data.get("id")
        instance.content = json_data.get("content")
        instance.public = json_data.get("public")
        instance.attachments = json_data.get("attachments")
        instance.author = json_data.get("author")
        return instance


class Employee(types.OkDeskBaseClass):
    """
     {
      "id": 3,
      "name": "Артамонов Анатолий Маратович",
      "group": {
        "id": 1,
        "name": "Отдел планирования"
      }
    }
    """

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.group: typing.Optional[types.IdNamePair] = None

    @classmethod
    def json_parse(cls, data: dict) -> "Employee":
        instance = cls()
        instance.id = data.get("id")
        instance.name = data.get("name")
        instance.group = data.get("group")
        return instance


class StatusTime(types.OkDeskBaseClass):
    """
    {
    "total": "134 д., 14 ч., 57 м.",
    "on_schedule_total": "36 д., 0 ч., 39 м."
    }
    """

    def __init__(self):
        self.total: str = None
        self.on_schedule_total: str = None

    @classmethod
    def json_parse(cls, data: dict) -> "StatusTime":
        instance = cls()
        instance.total = data.get("total")
        instance.on_schedule_total = data.get("on_schedule_total")
        return instance


class IssueType(types.OkDeskBaseClass):
    """
    {
        "id": 2,
        "code": "service",
        "name": "Обслуживание",
        "available_for_client": true
      }
    """

    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None
        self.available_for_client: bool = None

    @classmethod
    def json_parse(cls, data: dict) -> "IssueType":
        instance = cls()
        instance.id = data.get("id")
        instance.code = data.get("code")
        instance.name = data.get("name")
        instance.available_for_client = data.get("available_for_client")
        return instance


class Specification(types.OkDeskBaseClass):
    """{
      "id": 1,
      "name": "Доставка в сервис",
      "quantity": 1,
      "discount": 2,
      "total": 600,
      "comment": "",
      "total_vat": 343.83,
      "service": {
        "type": "service",
        "code": "timerateservice",
        "unit": "выезд"
      },
      "price_list": {
        "id": 2,
        "name": "Выездные услуги"
      },
      "performer": {
        "id": 3,
        "name": "Петров Иван Сергеевич"
      }
    }"""

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.quantity: float = None
        self.discount: float = None
        self.total: float = None
        self.comment: str = None
        self.total_vat: float = None
        self.service: dict = None
        self.price_list: types.IdNamePair = None
        self.performer: types.IdNamePair = None

    @classmethod
    def json_parse(cls, data: dict) -> "Specification":
        instance = cls()
        instance.id = data.get("id")
        instance.name = data.get("name")
        instance.quantity = data.get("quantity")
        instance.discount = data.get("discount")
        instance.total = data.get("total")
        instance.comment = data.get("comment")
        instance.total_vat = data.get("total_vat")
        instance.service = data.get("service")
        instance.price_list = data.get("price_list")
        instance.performer = data.get("performer")
        return instance


class TimeEntry(types.OkDeskBaseClass):
    """{
      "id": 1,
      "comment": "Упаковка",
      "spent_time": 1,
      "logged_at": "2018-10-16T11:14:00.000+03:00",
      "employee": {
        "id": 1,
        "login": "andrey@okdesk.ru",
        "name": "Елизаров Андрей Валерьевич"
      },
      "parameters": [
        {
          "code": "address",
          "name": "Адрес вызова",
          "field_type": "ftstring",
          "value": "ул. Ленина 44"
        }
      ]
    },"""

    def __init__(self):
        self.id: int = None
        self.comment: str = None
        self.spent_time: float = None
        self.logged_at: str = None
        self.employee: Employee = None
        self.parameters: typing.List[dict] = None

    @classmethod
    def json_parse(cls, data: dict) -> "TimeEntry":
        instance = cls()
        instance.id = data.get("id")
        instance.comment = data.get("comment")
        instance.spent_time = data.get("spent_time")
        instance.logged_at = data.get("logged_at")
        instance.employee = data.get("employee")
        instance.parameters = data.get("parameters")
        return instance


class CheckListItem(types.OkDeskBaseClass):
    """{
        "id": 1001,
        "name": "Проверить герметичность",
        "required": false,
        "visible_for_clients": true,
        "checked_at": "2021-01-27T20:45:00.703+03:00",
        "parameters": [
            {
                "param_type": "text",
                "required": true,
                "value": "Утечек не обнаружено"
            },
            {
                "param_type": "string",
                "required": true,
                "value": "51BKB835225"
            },
            {
                "param_type": "files",
                "required": false,
                "value": [
                    {
                        "id": 521,
                        "attachment_file_name": "check_photo.jpeg",
                        "attachment_file_size": 3243,
                        "created_at": "2021-04-23T17:20:27.937+03:00"
                    }
                ]
            }
        ],
        "item_type": "point",
        "parent_id": null,
        "planned_execution_in_hours": 1,
        "position": 1,
        "checked_by_user_id": 2,
        "checked": true
    }"""

    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.required: bool = None
        self.visible_for_clients: bool = None
        self.checked_at: str = None
        self.parameters: typing.List[dict] = None
        self.item_type: str = None
        self.parent_id: int = None
        self.planned_execution_in_hours: float = None
        self.position: int = None
        self.checked_by_user_id: int = None
        self.checked: bool = None

    @classmethod
    def json_parse(cls, data: dict) -> "CheckListItem":
        instance = cls()
        instance.id = data.get("id")
        instance.name = data.get("name")
        instance.required = data.get("required")
        instance.visible_for_clients = data.get("visible_for_clients")
        instance.checked_at = data.get("checked_at")
        instance.parameters = data.get("parameters")
        instance.item_type = data.get("item_type")
        instance.parent_id = data.get("parent_id")
        instance.planned_execution_in_hours = data.get("planned_execution_in_hours")
        instance.position = data.get("position")
        instance.checked_by_user_id = data.get("checked_by_user_id")
        instance.checked = data.get("checked")
        return instance


# issues


class Issue(types.OkDeskBaseClass):
    """
    {
      "id": 153,
      "title": "Требуется мастер на выезд",
      "description": "",
      "created_at": "2016-03-15T18:05:17.568+03:00",
      "completed_at": "2016-05-19T10:54:09.987+03:00",
      "deadline_at": "2019-09-24T14:35:00.000+03:00",
      "source": "from_employee",
      "spent_time_total": 0,
      "start_execution_until": "2016-03-16T09:05:17.568+03:00",
      "planned_execution_in_hours": 12,
      "planned_reaction_at": "2016-04-11T11:00:00.000+03:00",
      "reacted_at": "2016-04-10T18:43:44.951+03:00",
      "updated_at": "2016-08-23T09:39:35.428+03:00",
      "delayed_to": null,
      "company_id": 40,
      "group_id": 3,
      "coexecutors": [
        {
          "id": 3,
          "name": "Артамонов Анатолий Маратович",
          "group": {
            "id": 1,
            "name": "Отдел планирования"
          }
        }
      ],
      "service_object_id": null,
      "equipment_ids": [],
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
      "status_times": {
        "opened": {
          "total": "134 д., 14 ч., 57 м.",
          "on_schedule_total": "36 д., 0 ч., 39 м."
        },
        "completed": {
          "total": "0 д., 0 ч., 0 м.",
          "on_schedule_total": "0 д., 0 ч., 0 м."
        }
      },
      "parameters": [],
      "comments": {
        "count": 5,
        "last_at": "2018-07-05T16:06:10.000+03:00"
      },
      "parent_id": null,
      "child_ids": [],
      "type": {
        "id": 2,
        "code": "service",
        "name": "Обслуживание",
        "available_for_client": true
      },
      "priority": {
        "code": "low",
        "name": "Низкий"
      },
      "status": {
        "code": "opened",
        "name": "Открыта"
      },
      "old_status": {
        "code": "completed",
        "name": "Решена"
      },
      "rate": {
        "id": 3,
        "value": "normal"
      },
      "address": {
        "coordinates": [
          53.2184321,
          44.9998082
        ],
        "value": "г Пенза ул Гагарина д 13"
      },
      "observers": [
        {
          "id": 113,
          "type": "employee",
          "name": "Антонов Петр Захарович"
        },
        {
          "id": 121,
          "type": "employee",
          "name": "Акмаев Артем Викторович"
        }
      ],
      "observer_groups": [
        {
          "id": 5,
          "name": "Отдел контроля качества"
        }
      ],
      "contact": {
        "id": 3020,
        "name": "Егор Егоров"
      },
      "agreement": null,
      "assignee": {
        "id": 1,
        "name": "Иванов Иван Викторович"
      },
      "author": {
        "id": 3020,
        "name": "Егор Егоров"
      }
    }
    """

    def __init__(self):
        self.id: int = None
        self.title: str = None
        self.description: str = None
        self.created_at: datetime.datetime = None
        self.completed_at: datetime.datetime = None
        self.deadline_at: datetime.datetime = None
        self.source: str = None
        self.spent_time_total: int = None
        self.start_execution_until: datetime.datetime = None
        self.planned_execution_in_hours: int = None
        self.planned_reaction_at: datetime.datetime = None
        self.reacted_at: datetime.datetime = None
        self.updated_at: datetime.datetime = None
        self.delayed_to: datetime.datetime = None
        self.company_id: int = None
        self.group_id: int = None
        self.coexecutors: typing.List[Employee] = None
        self.service_object_id: int = None
        self.equipment_ids: typing.List[int] = None
        self.attachments: typing.List[shared.Attachment] = None
        self.status_times: dict[str, StatusTime] = None
        self.parameters: typing.List[dict] = None
        self.comments: dict = None
        self.parent_id: int = None
        self.child_ids: typing.List[int] = None
        self.type: IssueType = None
        self.priority: types.CodeNamePair = None
        self.status: types.CodeNamePair = None
        self.old_status: types.CodeNamePair = None
        self.rate: types.IdValuePair = None
        self.address: dict = None
        self.observers: typing.List[types.IdNameTypePair] = None
        self.observer_groups: typing.List[types.IdNamePair] = None
        self.contact: types.IdNamePair = None
        self.agreement: dict = None
        self.assignee: types.IdNamePair = None
        self.author: types.IdNamePair = None

    @classmethod
    def json_parse(cls, data: dict) -> "Issue":
        instance = cls()
        instance.id = data.get("id")
        instance.title = data.get("title")
        instance.description = data.get("description")
        created_at = data.get("created_at")
        if created_at:
            instance.created_at = datetime.datetime.fromisoformat(created_at)
        completed_at = data.get("completed_at")
        if completed_at:
            instance.completed_at = datetime.datetime.fromisoformat(completed_at)
        deadline_at = data.get("deadline_at")
        if deadline_at:
            instance.deadline_at = datetime.datetime.fromisoformat(deadline_at)
        instance.source = data.get("source")
        instance.spent_time_total = data.get("spent_time_total")
        start_execution_until = data.get("start_execution_until")
        if start_execution_until:
            instance.start_execution_until = datetime.datetime.fromisoformat(
                start_execution_until
            )
        instance.planned_execution_in_hours = data.get("planned_execution_in_hours")
        planned_reaction_at = data.get("planned_reaction_at")
        if planned_reaction_at:
            instance.planned_reaction_at = datetime.datetime.fromisoformat(
                planned_reaction_at
            )
        reacted_at = data.get("reacted_at")
        if reacted_at:
            instance.reacted_at = datetime.datetime.fromisoformat(reacted_at)
        updated_at = data.get("updated_at")
        if updated_at:
            instance.updated_at = datetime.datetime.fromisoformat(updated_at)
        delayed_to = data.get("delayed_to")
        if delayed_to:
            instance.delayed_to = datetime.datetime.fromisoformat(delayed_to)
        instance.company_id = data.get("company_id")
        instance.group_id = data.get("group_id")
        coexecutors = data.get("coexecutors")
        if coexecutors:
            instance.coexecutors = [
                Employee.json_parse(coexecutor) for coexecutor in coexecutors
            ]
        instance.service_object_id = data.get("service_object_id")
        instance.equipment_ids = data.get("equipment_ids")
        attachments = data.get("attachments")
        if attachments:
            instance.attachments = [
                shared.Attachment.json_parse(attachment) for attachment in attachments
            ]
        status_times = data.get("status_times")
        if status_times:
            instance.status_times = {
                key: StatusTime.json_parse(value) for key, value in status_times.items()
            }
        instance.parameters = data.get("parameters")
        instance.comments = data.get("comments")
        instance.parent_id = data.get("parent_id")
        instance.child_ids = data.get("child_ids")
        type_ = data.get("type")
        if type_:
            instance.type = IssueType.json_parse(type_)
        instance.priority = data.get("priority")
        instance.status = data.get("status")
        instance.old_status = data.get("old_status")
        instance.rate = data.get("rate")
        instance.address = data.get("address")
        instance.observers = data.get("observers")
        instance.observer_groups = data.get("observer_groups")
        instance.contact = data.get("contact")
        instance.agreement = data.get("agreement")
        instance.assignee = data.get("assignee")
        instance.author = data.get("author")
        return instance


class CreateIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!sozdanie-zayavki-sozdanie-zayavki

    POST /api/v1/issues/

    Название 	                    Тип 	            Обязательность 	Описание
    title 	                        string 	            обязательный 	Название заявки
    description 	                string 	            опционально 	Описание заявки
    company_id 	                    string 	            опционально 	ID компании, привязанной к заявке
    contact_id 	                    string 	            опционально 	ID контактного лица, привязанного к заявке
    agreement_id 	                string 	            опционально 	ID договора, привязанного к заявке
    assignee_id 	                string 	            опционально 	ID ответственного за заявку
    group_id 	                    string 	            опционально 	ID ответственной группы сотрудника
    observer_ids 	                array of integer 	опционально 	Массив из ID сотрудников, являющихся наблюдателями заявки
    observer_group_ids 	            array of integer 	опционально 	Массив из ID групп сотрудников, являющихся наблюдателями заявки
    contact_observer_ids 	        array of integer 	опционально 	Массив из ID контактных лиц, являющихся наблюдателями заявки
    maintenance_entity_id 	        string 	            опционально 	ID объекта обслуживания, привязанного к заявке
    equipment_ids 	                array 	            опционально 	Массив из ID оборудования, привязанного к заявке
    type 	                        string 	            опционально 	Код типа заявки
    priority 	                    string 	            опционально 	Код приоритета заявки
    deadline_at 	                string 	            опционально 	Плановая дата решения
    start_execution_until 	        string 	            опционально 	Назначена на (дата/время)
    planned_execution_in_minutes 	number 	            опционально 	Плановая продолжительность (в минутах)
    custom_parameters 	            associative array 	опционально 	Дополнительные атрибуты заявки
    parent_id 	                    string 	            опционально 	ID родительской заявки
    author 	                        associative array 	опционально 	Автор заявки. Для указания автора необходимо передать 2 параметра: id (ID автора, string, обязательный) и type (Тип автора, string, обязательный, допустимые значения: employee и contact). Параметр доступен только для ключей, связанных с пользовательской ролью “Администратор”.



    Обратите внимание
    Если Тип (type) или Приоритет (priority) пустые, то заявка будет создана с приоритетом и типом, установленными “по умолчанию” в настройках аккаунта.


    Допустимые параметры прикрепляемых файлов:
    Название 	    Тип 	Обязательность 	Описание
    attachment 	    string 	обязательный 	Прикрепляемый файл
    is_public 	    string 	опционально 	Публичность файла
    description 	string 	опционально 	Описание файла


    If files are present, the request must be sent as multipart/form-data. Otherwise, the request must be sent as application/json.
    Если в запросе присутствуют файлы, то запрос должен быть отправлен в формате multipart/form-data. В противном случае запрос должен быть отправлен в формате application/json.
    """

    def __init__(
        self,
        title: str,
        description: typing.Optional[str] = None,
        company_id: typing.Optional[str] = None,
        contact_id: typing.Optional[str] = None,
        agreement_id: typing.Optional[str] = None,
        assignee_id: typing.Optional[str] = None,
        group_id: typing.Optional[str] = None,
        observer_ids: typing.Optional[typing.List[int]] = None,
        observer_group_ids: typing.Optional[typing.List[int]] = None,
        contact_observer_ids: typing.Optional[typing.List[int]] = None,
        maintenance_entity_id: typing.Optional[str] = None,
        equipment_ids: typing.Optional[typing.List[str]] = None,
        type_: typing.Optional[str] = None,
        priority: typing.Optional[str] = None,
        deadline_at: typing.Optional[datetime.datetime] = None,
        start_execution_until: typing.Optional[datetime.datetime] = None,
        planned_execution_in_minutes: typing.Optional[float] = None,
        custom_parameters: typing.Optional[typing.List[dict]] = None,
        parent_id: typing.Optional[str] = None,
        author: typing.Optional[dict] = None,
        files: typing.Optional[typing.List[types.Attachment]] = None,
    ):
        """

        :param title: title of the request (Имя заявки)
        :param description: description of the request (Описание заявки)
        :param company_id: ID of the company (ID компании)
        :param contact_id: ID of the contact (ID контакта)
        :param agreement_id: ID of the agreement (ID договора)
        :param assignee_id: ID of the assignee (ID исполнителя)
        :param group_id: ID of the group (ID группы)
        :param observer_ids: IDs of the observers (ID наблюдателей)
        :param observer_group_ids: IDs of the observer groups (ID групп наблюдателей)
        :param contact_observer_ids: IDs of the contact observers (ID контактных наблюдателей)
        :param maintenance_entity_id: ID of the maintenance entity (ID объекта обслуживания)
        :param equipment_ids: IDs of the equipment (ID оборудования)
        :param type_: type of the request (Тип заявки)
        :param priority: priority of the request (Приоритет заявки)
        :param deadline_at: deadline of the request (Срок выполнения заявки)
        :param start_execution_until: start execution until (Начать выполнение до)
        :param planned_execution_in_minutes: planned execution in minutes (Планируемое время выполнения в минутах)
        :param custom_parameters: custom parameters (Пользовательские параметры)
        :param parent_id: ID of the parent request (ID родительской заявки)
        :param author: author of the request (Автор заявки)
        :param files: files to attach (Прикрепляемые файлы)
        """

        self.title: str = title
        self.description: typing.Optional[str] = description
        self.company_id: typing.Optional[str] = company_id
        self.contact_id: typing.Optional[str] = contact_id
        self.agreement_id: typing.Optional[str] = agreement_id
        self.assignee_id: typing.Optional[str] = assignee_id
        self.group_id: typing.Optional[str] = group_id
        self.observer_ids: typing.Optional[typing.List[int]] = observer_ids
        self.observer_group_ids: typing.Optional[typing.List[int]] = observer_group_ids
        self.contact_observer_ids: typing.Optional[
            typing.List[int]
        ] = contact_observer_ids
        self.maintenance_entity_id: typing.Optional[str] = maintenance_entity_id
        self.equipment_ids: typing.Optional[typing.List[str]] = equipment_ids
        self.type: typing.Optional[str] = type_
        self.priority: typing.Optional[str] = priority
        self.deadline_at: typing.Optional[datetime.datetime] = deadline_at
        self.start_execution_until: typing.Optional[
            datetime.datetime
        ] = start_execution_until
        self.planned_execution_in_minutes: typing.Optional[
            float
        ] = planned_execution_in_minutes
        self.custom_parameters: typing.Optional[typing.List[dict]] = custom_parameters
        self.parent_id: typing.Optional[str] = parent_id
        self.author: typing.Optional[dict] = author

        self.files: typing.Optional[typing.List[types.Attachment]] = files

    def to_request(self) -> dict:
        if not self.files:
            json_data = {
                "title": self.title,
            }
            if self.description:
                json_data["description"] = self.description
            if self.company_id:
                json_data["company_id"] = self.company_id
            if self.contact_id:
                json_data["contact_id"] = self.contact_id
            if self.agreement_id:
                json_data["agreement_id"] = self.agreement_id
            if self.assignee_id:
                json_data["assignee_id"] = self.assignee_id
            if self.group_id:
                json_data["group_id"] = self.group_id
            if self.observer_ids:
                json_data["observer_ids"] = self.observer_ids
            if self.observer_group_ids:
                json_data["observer_group_ids"] = self.observer_group_ids
            if self.contact_observer_ids:
                json_data["contact_observer_ids"] = self.contact_observer_ids
            if self.maintenance_entity_id:
                json_data["maintenance_entity_id"] = self.maintenance_entity_id
            if self.equipment_ids:
                json_data["equipment_ids"] = self.equipment_ids
            if self.type:
                json_data["type"] = self.type
            if self.priority:
                json_data["priority"] = self.priority
            if self.deadline_at:
                json_data["deadline_at"] = helpers.convert_param(self.deadline_at)
            if self.start_execution_until:
                json_data["start_execution_until"] = helpers.convert_param(
                    self.start_execution_until
                )
            if self.planned_execution_in_minutes:
                json_data[
                    "planned_execution_in_minutes"
                ] = self.planned_execution_in_minutes
            if self.custom_parameters:
                json_data["custom_parameters"] = self.custom_parameters
            if self.parent_id:
                json_data["parent_id"] = self.parent_id
            if self.author:
                json_data["author"] = self.author
            return {
                "method": "POST",
                "url": "api/v1/issues/",
                "json": {"issue": json_data},
            }
        else:
            multipart = MultipartEncoder(
                fields={
                    "issue[title]": self.title,
                }
            )
            if self.description:
                multipart.fields["issue[description]"] = self.description
            if self.company_id:
                multipart.fields["issue[company_id]"] = self.company_id
            if self.contact_id:
                multipart.fields["issue[contact_id]"] = self.contact_id
            if self.agreement_id:
                multipart.fields["issue[agreement_id]"] = self.agreement_id
            if self.assignee_id:
                multipart.fields["issue[assignee_id]"] = self.assignee_id
            if self.group_id:
                multipart.fields["issue[group_id]"] = self.group_id
            if self.observer_ids:
                multipart.fields["issue[observer_ids][]"] = [
                    str(i) for i in self.observer_ids
                ]
            if self.observer_group_ids:
                multipart.fields["issue[observer_group_ids][]"] = [
                    str(i) for i in self.observer_group_ids
                ]
            if self.contact_observer_ids:
                multipart.fields["issue[contact_observer_ids][]"] = [
                    str(i) for i in self.contact_observer_ids
                ]
            if self.maintenance_entity_id:
                multipart.fields[
                    "issue[maintenance_entity_id]"
                ] = self.maintenance_entity_id
            if self.equipment_ids:
                multipart.fields["issue[equipment_ids][]"] = [
                    str(i) for i in self.equipment_ids
                ]
            if self.type:
                multipart.fields["issue[type]"] = self.type
            if self.priority:
                multipart.fields["issue[priority]"] = self.priority
            if self.deadline_at:
                multipart.fields["issue[deadline_at]"] = helpers.convert_param(
                    self.deadline_at
                )
            if self.start_execution_until:
                multipart.fields["issue[start_execution_until]"] = str(
                    self.start_execution_until
                )
            if self.planned_execution_in_minutes:
                multipart.fields["issue[planned_execution_in_minutes]"] = str(
                    self.planned_execution_in_minutes
                )
            if self.custom_parameters:
                multipart.fields["issue[custom_parameters][]"] = [
                    str(i) for i in self.custom_parameters
                ]
            if self.parent_id:
                multipart.fields["issue[parent_id]"] = self.parent_id
            if self.author:
                multipart.fields["issue[author]"] = str(self.author)
            for i, file in enumerate(self.files):
                if "description" in file:
                    multipart.fields[
                        f"issue[files_attributes][{i}][description]"
                    ] = file["description"]
                if "is_public" in file:
                    multipart.fields[
                        f"issue[files_attributes][{i}][is_public]"
                    ] = helpers.convert_param(file["is_public"])
                f_name = file["attachment"]
                if not os.path.isfile(f_name):
                    raise Exception(f"File {f_name} not found in the filesystem")
                name = os.path.basename(f_name)
                mime = mimetypes.guess_type(f_name)[0]
                multipart.fields[f"issue[files_attributes][{i}][attachment]"] = (
                    name,
                    open(f_name, "rb"),
                    mime,
                )
            return {
                "method": "POST",
                "url": "api/v1/issues/",
                "data": multipart.read(),
                "headers": {
                    "Content-Type": multipart.content_type,
                },
            }

    def from_response(self, result) -> int:
        return result["id"]


class ChangeIssueAssigneeRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!smena-otvetstvennogo-smena-otvetstvennogo-za-zayavku

    PATCH /api/v1/issues/{issue_id}/assignees

    Название 	    Тип 	Обязательность 	Описание
    assignee_id 	string 	опционально 	ID ответственного за заявку
    group_id 	    string 	опционально 	ID ответственной группы

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)
    """

    def __init__(
        self,
        issue_id: int,
        assignee_id: typing.Optional[int] = None,
        group_id: typing.Optional[int] = None,
    ):
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param assignee_id: ID of the assignee (optional) (ID ответственного за заявку)
        :param group_id: ID of the group (optional) (ID ответственной группы)
        """
        self.issue_id: int = issue_id
        self.assignee_id: typing.Optional[int] = assignee_id
        self.group_id: typing.Optional[int] = group_id

    def to_request(self) -> dict:
        json_data = {}
        if self.assignee_id:
            json_data["assignee_id"] = self.assignee_id
        if self.group_id:
            json_data["group_id"] = self.group_id
        return {
            "method": "PATCH",
            "url": f"api/v1/issues/{self.issue_id}/assignees",
            "json": json_data,
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class ChangeIssueDeadlineRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!smena-planovoj-daty-resheniya-smena-planovoj-daty-resheniya-zayavki
    PATCH /api/v1/issues/{issue_id}/deadlines

    Название 	    Тип 	Обязательность 	Описание
    deadline_at 	string 	опционально 	Планируемая дата решения заявки

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)

    """

    def __init__(
        self,
        issue_id: int,
        deadline_at: typing.Optional[datetime.datetime] = None,
    ):
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param deadline_at:  (optional) (Планируемая дата решения заявки)
        """
        self.issue_id: int = issue_id
        self.deadline_at: typing.Optional[datetime.datetime] = deadline_at

    def to_request(self) -> dict:
        json_data = {}
        if self.deadline_at:
            json_data["deadline_at"] = self.deadline_at.strftime("%Y-%m-%d %H:%M")
        return {
            "method": "PATCH",
            "url": f"api/v1/issues/{self.issue_id}/deadlines",
            "json": json_data,
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class ChangeIssueCodeRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!smena-tipa-zayavki-smena-tipa-zayavki

    PATCH /api/v1/issues/{issue_id}/types

    Название 	Тип 	Обязательность 	Описание
    code 	    string 	обязательный 	Код типа заявки

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)

    """

    def __init__(
        self,
        issue_id: int,
        code: str,
    ):
        """

        :param issue_id: ID of the issue   (ID заявки )
        :param code: Code of the issue type (Код типа заявки)
        """
        self.issue_id: int = issue_id
        self.code: str = code

    def to_request(self) -> dict:
        return {
            "method": "PATCH",
            "url": f"api/v1/issues/{self.issue_id}/types",
            "json": {
                "code": self.code,
            },
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class ChangeIssueParametersRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!redaktirovanie-dopolnitelnyh-atributov-zayavki-redaktirovanie-dopolnitelnyh-atributov-zayavki

    PATCH api/v1/issues/{issue_id}/parameters

    Название 	Тип 	Обязательность 	Описание
    custom_parameters 	dict 	обязательный 	Объект с параметрами заявки

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)

    """

    def __init__(
        self,
        issue_id: int,
        custom_parameters: typing.Dict[str, typing.Any],
    ):
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param custom_parameters:  Custom parameters of the issue (Объект с параметрами заявки)
        """
        self.issue_id: int = issue_id
        self.custom_parameters: typing.Dict[str, typing.Any] = custom_parameters

    def to_request(self) -> dict:
        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/parameters",
            "json": {
                "custom_parameters": self.custom_parameters,
            },
            "allow_non_json": True,
        }

    def from_response(self, result) -> None:
        return None


class ChangeIssueAddressRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!redaktirovanie-adresa-redaktirovanie-adresa-zayavki

    PATCH api/v1/issues/{issue_id}/addresses

    Название 	    Тип 	        Обязательность 	Описание
    value 	        string 	        обязательный 	Строковое представление адреса заявки
    coordinates 	array of float 	обязательный 	Координаты адреса заявки

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)

    """

    def __init__(
        self,
        issue_id: int,
        value: str,
        coordinates: typing.List[float],
    ):
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param value:  String representation of the issue address (Строковое представление адреса заявки)
        :param coordinates:  Coordinates of the issue address (Координаты адреса заявки)
        """
        self.issue_id: int = issue_id
        self.value: str = value
        self.coordinates: typing.List[float] = coordinates

    def to_request(self) -> dict:
        return {
            "method": "PATCH",
            "url": f"api/v1/issues/{self.issue_id}/addresses",
            "json": {
                "value": self.value,
                "coordinates": self.coordinates,
            },
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class ChangeIssueStatusRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!status-zayavki-smena-statusa-zayavki
    POST /api/v1/issues/{issue_id}/statuses

    Название 	        Тип 	            Обязательность 	Описание
    code 	            string 	            обязательный 	Код статуса
    delay_to 	        string 	            опционально 	Время, до которого откладывается заявка. Обязательное поле только для статуса delayed. Для остальных статусов данный параметр будет игнорироваться.
    comment 	        string 	            опционально 	Комментарий к статусу. Например, причина перехода в новый статус. Обязательность данного параметра настраивается в разделе “Настройки/Заявки/Статусы заявок”.
    comment_public 	    boolean 	        опционально 	Флаг публичности комментария. Принимает значение true или false
    custom_parameters 	associative array 	опционально 	Дополнительные атрибуты заявки, которые доступны пользователю для заполнения при входе в новый или при выходе из текущего статуса.
    time_entry 	        array 	            опционально 	Массив трудозатрат по заявке, которые будут добавлены при смене статуса
    skip_options 	    array 	            опционально 	Массив флагов, позволяющих пропустить отправку оповещений (skip_notifications), вебхуков (skip_webhooks), автоматических действий (skip_triggers)

    issue_id - ID of the issue (required)
    issue_id - ID заявки (обязательно)

    !!!
    Параметр delay_to является обязательным для перехода в статус delayed
    Параметр comment по умолчанию обязателен для статуса delayed
    Для смены статуса заявки в настройках вашего аккаунта должен быть разрешен переход из текущего статуса заявки в статус, передаваемый в запросе
    Параметр formatted_spent_time передается в формате 2 ч. 30 мин. или 2:30 или 2,5 часа и т.д.

    """

    def __init__(
        self,
        issue_id: int,
        code: str,
        delay_to: typing.Optional[datetime.datetime] = None,
        comment: typing.Optional[str] = None,
        comment_public: typing.Optional[bool] = None,
        custom_parameters: typing.Optional[dict] = None,
        time_entry: typing.Optional[list] = None,
        skip_options: typing.Optional[list] = None,
    ):
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param code: Code of the status (required) (Код статуса (обязательно))
        :param delay_to: Time, until which the application is postponed. Required only for the delayed status. For the rest of the statuses, this parameter will be ignored. (Время, до которого откладывается заявка. Обязательное поле только для статуса delayed. Для остальных статусов данный параметр будет игнорироваться.)
        :param comment: Comment to the status. For example, the reason for the transition to a new status. The necessity of this parameter is configured in the section “Settings / Tickets / Ticket Statuses”. (Комментарий к статусу. Например, причина перехода в новый статус. Обязательность данного параметра настраивается в разделе “Настройки/Заявки/Статусы заявок”.)
        :param comment_public: Flag of the publicness of the comment. Takes the value true or false (Флаг публичности комментария. Принимает значение true или false)
        :param custom_parameters: Additional attributes of the application that the user can fill in when entering a new or exiting the current status. (Дополнительные атрибуты заявки, которые доступны пользователю для заполнения при входе в новый или при выходе из текущего статуса.)
        :param time_entry: Array of time entries for the application that will be added when changing the status (Массив трудозатрат по заявке, которые будут добавлены при смене статуса)
        :param skip_options: Array of flags that allow you to skip sending notifications (skip_notifications), webhooks (skip_webhooks), automatic actions (skip_triggers) (Массив флагов, позволяющих пропустить отправку оповещений (skip_notifications), вебхуков (skip_webhooks), автоматических действий (skip_triggers))
        """
        self.issue_id: int = issue_id
        self.code: str = code
        self.delay_to: typing.Optional[datetime.datetime] = delay_to
        self.comment: typing.Optional[str] = comment
        self.comment_public: typing.Optional[bool] = comment_public
        self.custom_parameters: typing.Optional[dict] = custom_parameters
        self.time_entry: typing.Optional[list] = time_entry
        self.skip_options: typing.Optional[list] = skip_options

    def to_request(self) -> dict:
        json_dict = {
            "code": self.code,
        }
        if self.delay_to is not None:
            json_dict["delay_to"] = self.delay_to.isoformat()
        if self.comment is not None:
            json_dict["comment"] = self.comment
        if self.comment_public is not None:
            json_dict["comment_public"] = self.comment_public
        if self.custom_parameters is not None:
            json_dict["custom_parameters"] = self.custom_parameters
        if self.time_entry is not None:
            json_dict["time_entry"] = self.time_entry
        if self.skip_options is not None:
            json_dict["skip_options"] = self.skip_options

        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/statuses",
            "json": json_dict,
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class AddCommentRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!kommentarii-dobavlenie-kommentariya

    POST /api/v1/issues/{issue_id}/comments

    Название 	        Тип 	    Обязательность 	Описание
    content 	        string 	    обязательный 	Текст комментария. Текст комментария является html-текстом, а значит требуемое форматирование необходимо задавать с использованием html-тегов. Например, для переноса строк необходимо использовать тег </br>
    author_id 	        integer 	обязательный 	ID пользователя, являющегося автором комментария

    author_type 	    string 	    опционально 	Тип пользователя, являющегося автором комменатрия
    Допустимые типы:    'employee'                    (по умолчанию) сотрудник
                        'contact'                     контактное лицо

    public 	            boolean 	опционально 	Флаг публичности комментария. Принимает значение true или false
    attachments 	    array 	    опционально 	Список приложенных файлов
    """

    def __init__(
        self,
        issue_id: int,
        content: str,
        author_id: int,
        author_type: typing.Optional[typing.Literal["employee", "contact"]] = None,
        public: typing.Optional[bool] = None,
        attachments: typing.Optional[typing.List[types.Attachment]] = None,
    ):
        """

        :param issue_id: Issue ID (ID обращения)
        :param content: Comment text. Comment text is html text, so the required formatting must be specified using html tags. For example, to break lines, you must use the </br> tag (Текст комментария. Текст комментария является html-текстом, а значит требуемое форматирование необходимо задавать с использованием html-тегов. Например, для переноса строк необходимо использовать тег </br>)
        :param author_id: User ID (ID пользователя)
        :param author_type: User type (Тип пользователя)
        :param public: Public flag (Флаг публичности комментария)
        :param attachments: List of attached files (Список приложенных файлов)
        """

        self.issue_id: int = issue_id
        self.content: str = content
        self.author_id: int = author_id
        self.author_type: typing.Optional[
            typing.Literal["employee", "contact"]
        ] = author_type
        self.public: typing.Optional[bool] = public
        self.attachments: typing.Optional[typing.List[types.Attachment]] = attachments

    def to_request(self) -> dict:
        if self.attachments is None:
            json_dict = {"content": self.content}
            if self.author_id is not None:
                json_dict["author_id"] = self.author_id
            if self.author_type is not None:
                json_dict["author_type"] = self.author_type
            if self.public is not None:
                json_dict["public"] = self.public
            if self.attachments is not None:
                json_dict["attachments"] = self.attachments
            return {
                "method": "POST",
                "url": f"api/v1/issues/{self.issue_id}/comments",
                "json": {"comment": json_dict},
            }
        else:
            multipart = MultipartEncoder({})
            multipart.fields["comment[content]"] = self.content
            if self.author_id is not None:
                multipart.fields["comment[author_id]"] = self.author_id
            if self.author_type is not None:
                multipart.fields["comment[author_type]"] = self.author_type
            if self.public is not None:
                multipart.fields["comment[public]"] = self.public
            for i, attachment in enumerate(self.attachments):
                multipart.fields[f"comment[attachments_attributes][{i}][file]"] = (
                    os.path.basename(attachment["attachment"]),
                    open(attachment["attachment"], "rb"),
                    mimetypes.guess_type(attachment["attachment"])[0],
                )
                if "description" in attachment:
                    multipart.fields[
                        f"comment[attachments_attributes][{i}][description]"
                    ] = attachment["description"]
            return {
                "method": "POST",
                "url": f"api/v1/issues/{self.issue_id}/comments",
                "data": multipart.read(),
                "headers": {
                    "Content-Type": multipart.content_type,
                },
            }

    def from_response(self, result) -> Comment:
        return Comment.json_parse(result)


class GetCommentsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!kommentarii-poluchenie-spiska-kommentariev
    GET api/v1/issues/{issue_id}/comments


    """

    def __init__(self, issue_id: int):
        """

        :param issue_id: Issue ID (ID обращения)
        """
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/comments",
        }

    def from_response(self, result) -> typing.List[Comment]:
        return [Comment.json_parse(item) for item in result]


class GetIssuesListIdRequest(types.ApiRequest):
    """
    returns array of issue ids!
    https://okdesk.ru/apidoc#!poluchenie-spiska-po-parametram-poluchenie-spiska-po-parametram

    GET /api/v1/issues/count

    Название 	            Тип 	            Обязательность 	Описание
    assignee_ids 	        array of integer 	опционально 	Массив из ID сотрудников, которые являются ответственными за заявки (для отображения заявок без ответственного необходимо передавать в параметре значение “0”).
    Пример: assignee_ids[]=1&assignee_ids[]=2

    assignee_group_ids 	    array of integer 	опционально 	Массив из ID ответственных групп (для отображения заявок без ответственной группы необходимо передавать в параметре значение “0”).
    Пример: assignee_group_ids[]=1&assignee_group_ids[]=2

    company_ids 	        array of integer 	опционально 	Массив из ID компаний, которые являются клиентами заявок (для отображения заявок без компании необходимо передавать в параметре значение “0”).
    Пример: company_ids[]=1&company_ids[]=2

    agreement_ids 	        array of integer 	опционально 	Массив из ID договоров (для отображения заявок без договоров необходимо передавать в параметре значение “0”).
    Пример: agreement_ids[]=1&agreement_ids[]=2

    contact_ids 	        array of integer 	опционально 	Массив из ID пользователей, которые являются контактными лицами заявок (для отображения заявок без контактного лица необходимо передавать в параметре значение “0”).
    Пример: contact_ids[]=1&contact_ids[]=2

    author_employee_ids 	array of integer 	опционально 	Массив из ID сотрудников, которые являются авторами заявок (для отображения заявок без автора необходимо передавать в параметре значение “0”).
    Пример: author_employee_ids[]=1

    Сочетается с параметром author_contact_ids по правилу ИЛИ
    author_contact_ids 	    array of integer 	опционально 	Массив из ID контактных лиц, которые являются авторами заявок (для отображения заявок без автора необходимо передавать в параметре значение “0”).
    Пример: author_contact_ids[]=57
    Сочетается с параметром author_employee_ids по правилу ИЛИ

    maintenance_entity_ids 	array of integer 	опционально 	Массив из ID объектов обслуживания, которые связаны с заявками.
    Пример: maintenance_entity_ids[]=1

    equipment_ids 	        array of integer 	опционально 	Массив из ID оборудования, которое связано с заявками (для отображения заявок без оборудования необходимо передавать в параметре значение “0”).
    Пример: equipment_ids[]=4

    status 	                array of string 	опционально 	Массив из Кодов статусов заявок
    Пример: status[]=opened&status[]=completed

    status_not 	            array of string 	опционально 	Массив из Кодов статусов заявок, в которых не должна находится заявка
    Пример: status_not[]=opened&status_not[]=completed

    opened 	                boolean 	        опционально 	Флаг "Открытые заявки". Если значение поля будет равно true, то в выборку не попадут заявки в статусах, для которых указано значение “Заявки в этом статусе считаются выполненными”.

    priority 	            array of string 	опционально 	Массив из Кодов приоритетов заявок
    Пример: priority[]=high&priority[]=low

    type 	                array of string 	опционально 	Массив из Кодов типов заявок
    Пример: type[]=incident

    rate 	                array of string 	опционально 	Массив из Значений оценок заявок (для отображения заявок без оценок необходимо передавать в параметре значение “0”).
    Пример: rate[]=bad&rate[]=normal&rate[]=good

    created_since 	        string 	            опционально 	Дата создания заявки (С)
    Пример: created_since=22-03-2016

    created_until 	        string 	            опционально 	Дата создания заявки (По)
    Пример: created_until=22-06-2016

    overdue 	            integer 	        опционально 	Флаг "Просроченные заявки по времени решения". Если значение поля будет равно 1, то в выборку попадут только просроченные по времени решения заявки. Если значение поля будет равно 0, то в выборку попадут все заявки
    Пример: overdue=0

    overdue_reaction 	    integer 	        опционально 	Флаг "Просроченные заявки по времени реакции". Если значение поля будет равно 1, то в выборку попадут только просроченные по времени реакции заявки. Если значение поля будет равно 0, то в выборку попадут все заявки
    Пример: overdue_reaction=0

    completed_since 	    string 	            опционально 	Дата решения заявки (С)
    Пример: completed_since=22-03-2018

    completed_until 	    string 	            опционально 	Дата решения заявки (По)
    Пример: completed_until=22-06-2018

    updated_since 	        string 	            опционально 	Дата последнего изменения заявки (С)
    Пример: updated_since=03-12-2018

    updated_until 	        string 	            опционально 	Дата последнего изменения заявки (По)
    Пример: updated_until=03-12-2018

    reacted_since 	        string 	            опционально 	Фактическое время реакции (С)
    Пример: reacted_since=03-12-2018 15:30

    reacted_until 	        string 	            опционально 	Фактическое время реакции (По)
    Пример: reacted_until=06-12-2018 18:00

    deadline_since 	        string 	            опционально 	Плановая дата решения заявки (С)
    Пример: deadline_since=03-12-2018 15:30

    deadline_until 	        string              опционально 	Плановая дата решения заявки (По)
    Пример: deadline_until=06-12-2018 18:00

    start_execution_since 	string 	            опционально 	Назначена на (С)
    Пример: start_execution_since=05-07-2021 11:30

    start_execution_until 	string 	            опционально 	Назначена на (По)
    Пример: start_execution_until=06-07-2021 00:00

    planned_reaction_since 	string 	            опционально 	Плановое время реакции (С)
    Пример: planned_reaction_since=05-07-2021 11:30

    planned_reaction_until 	string 	            опционально 	Плановое время реакции (По)
    Пример: planned_reaction_until=06-07-2021 00:00

    custom_parameters 	    associative array 	опционально 	Ассоциативный массив из пар Код дополнительного атрибута: Значение или набор значений

    """

    def __init__(
        self,
        assignee_ids: typing.Optional[typing.List[int]] = None,
        assignee_group_ids: typing.Optional[typing.List[int]] = None,
        company_ids: typing.Optional[typing.List[int]] = None,
        agreement_ids: typing.Optional[typing.List[int]] = None,
        contact_ids: typing.Optional[typing.List[int]] = None,
        author_employee_ids: typing.Optional[typing.List[int]] = None,
        author_contact_ids: typing.Optional[typing.List[int]] = None,
        maintenance_entity_ids: typing.Optional[typing.List[int]] = None,
        equipment_ids: typing.Optional[typing.List[int]] = None,
        status: typing.Optional[typing.List[str]] = None,
        status_not: typing.Optional[typing.List[str]] = None,
        opened: typing.Optional[bool] = None,
        priority: typing.Optional[typing.List[str]] = None,
        type_: typing.Optional[typing.List[str]] = None,
        rate: typing.Optional[typing.List[str]] = None,
        created_since: typing.Optional[datetime.date] = None,
        created_until: typing.Optional[datetime.date] = None,
        overdue: typing.Optional[int] = None,
        overdue_reaction: typing.Optional[int] = None,
        completed_since: typing.Optional[datetime.date] = None,
        completed_until: typing.Optional[datetime.date] = None,
        updated_since: typing.Optional[datetime.date] = None,
        updated_until: typing.Optional[datetime.date] = None,
        reacted_since: typing.Optional[datetime.datetime] = None,
        reacted_until: typing.Optional[datetime.datetime] = None,
        deadline_since: typing.Optional[datetime.datetime] = None,
        deadline_until: typing.Optional[datetime.datetime] = None,
        start_execution_since: typing.Optional[datetime.datetime] = None,
        start_execution_until: typing.Optional[datetime.datetime] = None,
        planned_reaction_since: typing.Optional[datetime.datetime] = None,
        planned_reaction_until: typing.Optional[datetime.datetime] = None,
        custom_parameters: typing.Optional[typing.List[helpers.AttributeFilter]] = None,
    ):
        """

        :param assignee_ids: IDs of employees who are responsible for the ticket (ID ответственных сотрудников)
        :param assignee_group_ids: IDs of employee groups who are responsible for the ticket (ID ответственных групп сотрудников)
        :param company_ids: IDs of companies (ID компаний)
        :param agreement_ids: IDs of agreements (ID договоров)
        :param contact_ids: IDs of contacts (ID контактов)
        :param author_employee_ids: IDs of employees who created the ticket (ID авторов заявки)
        :param author_contact_ids: IDs of contacts who created the ticket (ID контактов авторов заявки)
        :param maintenance_entity_ids: IDs of maintenance entities (ID объектов обслуживания)
        :param equipment_ids: IDs of equipment (ID оборудования)
        :param status: Statuses of tickets (Статусы заявок)
        :param status_not: Statuses of tickets to exclude (Статусы заявок для исключения)
        :param opened: Opened tickets (Открытые заявки)
        :param priority: Priorities of tickets (Приоритеты заявок)
        :param type_: Types of tickets (Типы заявок)
        :param rate: Rates of tickets (Рейтинг заявок)
        :param created_since: Date of creation (С)
        :param created_until: Date of creation (По)
        :param overdue: Overdue tickets (Просроченные заявки)
        :param overdue_reaction: Overdue reaction tickets (Просроченные заявки на реакцию)
        :param completed_since: Date of completion since (Дата завершения С)
        :param completed_until: Date of completion until (Дата завершения По)
        :param updated_since: Date of last update since (Дата последнего обновления С)
        :param updated_until: Date of last update until (Дата последнего обновления По)
        :param reacted_since: Datetime of last reaction since (Дата-время последней реакции С)
        :param reacted_until: Datetime of last reaction until (Дата-время последней реакции По)
        :param deadline_since: Datetime of deadline since (Дата-время дедлайна С)
        :param deadline_until: Datetime of deadline until (Дата-время дедлайна По)
        :param start_execution_since: Datetime of start execution since (Дата-время начала выполнения С)
        :param start_execution_until: Datetime of start execution until (Дата-время начала выполнения По)
        :param planned_reaction_since: Datetime of planned reaction since (Дата-время планируемой реакции С)
        :param planned_reaction_until: Datetime of planned reaction until (Дата-время планируемой реакции По)
        :param custom_parameters: Custom parameters (Пользовательские параметры)
        """

        self.assignee_ids: typing.Optional[typing.List[int]] = assignee_ids
        self.assignee_group_ids: typing.Optional[typing.List[int]] = assignee_group_ids
        self.company_ids: typing.Optional[typing.List[int]] = company_ids
        self.agreement_ids: typing.Optional[typing.List[int]] = agreement_ids
        self.contact_ids: typing.Optional[typing.List[int]] = contact_ids
        self.author_employee_ids: typing.Optional[
            typing.List[int]
        ] = author_employee_ids
        self.author_contact_ids: typing.Optional[typing.List[int]] = author_contact_ids
        self.maintenance_entity_ids: typing.Optional[
            typing.List[int]
        ] = maintenance_entity_ids
        self.equipment_ids: typing.Optional[typing.List[int]] = equipment_ids
        self.status: typing.Optional[typing.List[str]] = status
        self.status_not: typing.Optional[typing.List[str]] = status_not
        self.opened: typing.Optional[bool] = opened
        self.priority: typing.Optional[typing.List[str]] = priority
        self.type: typing.Optional[typing.List[str]] = type_
        self.rate: typing.Optional[typing.List[str]] = rate
        self.created_since: typing.Optional[datetime.datetime] = created_since
        self.created_until: typing.Optional[datetime.datetime] = created_until
        self.overdue: typing.Optional[bool] = overdue
        self.overdue_reaction: typing.Optional[bool] = overdue_reaction
        self.completed_since: typing.Optional[datetime.date] = completed_since
        self.completed_until: typing.Optional[datetime.date] = completed_until
        self.updated_since: typing.Optional[datetime.date] = updated_since
        self.updated_until: typing.Optional[datetime.date] = updated_until
        self.reacted_since: typing.Optional[datetime.datetime] = reacted_since
        self.reacted_until: typing.Optional[datetime.datetime] = reacted_until
        self.deadline_since: typing.Optional[datetime.datetime] = deadline_since
        self.deadline_until: typing.Optional[datetime.datetime] = deadline_until
        self.start_execution_since: typing.Optional[
            datetime.datetime
        ] = start_execution_since
        self.start_execution_until: typing.Optional[
            datetime.datetime
        ] = start_execution_until
        self.planned_reaction_since: typing.Optional[
            datetime.datetime
        ] = planned_reaction_since
        self.planned_reaction_until: typing.Optional[
            datetime.datetime
        ] = planned_reaction_until
        self.custom_parameters: typing.Optional[
            typing.List[helpers.AttributeFilter]
        ] = custom_parameters

    def to_request(self) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.assignee_ids:
            params["assignee_ids[]"] = [str(i) for i in self.assignee_ids]
        if self.assignee_group_ids:
            params["assignee_group_ids[]"] = [str(i) for i in self.assignee_group_ids]
        if self.company_ids:
            params["company_ids[]"] = [str(i) for i in self.company_ids]
        if self.agreement_ids:
            params["agreement_ids[]"] = [str(i) for i in self.agreement_ids]
        if self.contact_ids:
            params["contact_ids[]"] = [str(i) for i in self.contact_ids]
        if self.author_employee_ids:
            params["author_employee_ids[]"] = [str(i) for i in self.author_employee_ids]
        if self.author_contact_ids:
            params["author_contact_ids[]"] = [str(i) for i in self.author_contact_ids]
        if self.maintenance_entity_ids:
            params["maintenance_entity_ids[]"] = [
                str(i) for i in self.maintenance_entity_ids
            ]
        if self.equipment_ids:
            params["equipment_ids[]"] = [str(i) for i in self.equipment_ids]
        if self.status:
            params["status[]"] = [str(i) for i in self.status]
        if self.status_not:
            params["status_not[]"] = [str(i) for i in self.status_not]
        if self.opened is not None:
            params["opened"] = str(self.opened).lower()
        if self.priority:
            params["priority[]"] = [str(i) for i in self.priority]
        if self.type:
            params["type[]"] = [str(i) for i in self.type]
        if self.rate:
            params["rate[]"] = [str(i) for i in self.rate]
        if self.created_since:
            params["created_since"] = self.created_since.isoformat()
        if self.created_until:
            params["created_until"] = self.created_until.isoformat()
        if self.overdue is not None:
            params["overdue"] = str(self.overdue).lower()
        if self.overdue_reaction is not None:
            params["overdue_reaction"] = str(self.overdue_reaction).lower()
        if self.completed_since:
            params["completed_since"] = self.completed_since.strftime("%Y-%m-%d")
        if self.completed_until:
            params["completed_until"] = self.completed_until.strftime("%Y-%m-%d")
        if self.updated_since:
            params["updated_since"] = self.updated_since.strftime("%Y-%m-%d")
        if self.updated_until:
            params["updated_until"] = self.updated_until.strftime("%Y-%m-%d")
        if self.reacted_since:
            params["reacted_since"] = self.reacted_since.isoformat()
        if self.reacted_until:
            params["reacted_until"] = self.reacted_until.isoformat()
        if self.deadline_since:
            params["deadline_since"] = self.deadline_since.isoformat()
        if self.deadline_until:
            params["deadline_until"] = self.deadline_until.isoformat()
        if self.start_execution_since:
            params["start_execution_since"] = self.start_execution_since.isoformat()
        if self.start_execution_until:
            params["start_execution_until"] = self.start_execution_until.isoformat()
        if self.planned_reaction_since:
            params["planned_reaction_since"] = self.planned_reaction_since.isoformat()
        if self.planned_reaction_until:
            params["planned_reaction_until"] = self.planned_reaction_until.isoformat()
        if self.custom_parameters:
            params.update(
                helpers.convert_additional_attributes_filter(
                    "custom_parameters", self.custom_parameters
                )
            )
        return {
            "method": "GET",
            "url": "api/v1/issues/count",
            "params": params,
        }

    def from_response(self, result) -> typing.List[int]:
        return result


class GetIssuesListRichRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-detalizirovannogo-spiska-po-parametram-poluchenie-detalizirovannogo-spiska-po-parametram
    GET /api/v1/issues/list

    Название 	        Тип 	            Обязательность 	Описание
    company_ids 	    array of integer 	опционально 	Массив из ID компаний, которые являются клиентами заявок (для отображения заявок без компании необходимо передавать в параметре значение “0”).
    Пример: company_ids[]=1&company_ids[]=2

    contact_ids 	    array of integer 	опционально 	Массив из ID пользователей, которые являются контактными лицами заявок (для отображения заявок без контактного лица необходимо передавать в параметре значение “0”).
    Пример: contact_ids[]=1&contact_ids[]=2

    service_object_ids 	array of integer 	опционально 	Массив из ID объектов обслуживания, которые связаны с заявками (для отображения заявок без объекта обслуживания необходимо передавать в параметре значение “0”)
    Пример: service_object_ids[]=1

    status_codes 	    array of string 	опционально 	Массив из Кодов статусов заявок
    Пример: status_codes[]=opened&status_codes[]=completed

    priority_codes 	    array of string 	опционально 	Массив из Кодов приоритетов заявок
    Пример: priority_codes[]=high&priority_codes[]=low

    type_codes 	        array of string 	опционально 	Массив из Кодов типов заявок
    Пример: type_codes[]=incident

    created_since 	    string          	опционально 	Дата создания заявки (С)
    Пример: created_since=22-03-2022

    created_until 	    string          	опционально 	Дата создания заявки (По)
    Пример: created_until=22-06-2022

    completed_since 	string 	            опционально 	Дата решения заявки (С)
    Пример: completed_since=22-03-2022

    completed_until 	string              опционально 	Дата решения заявки (По)
    Пример: completed_until=22-06-2022


    ==============
    pages
    Название 	        Тип 	            Обязательность 	Описание
    number 	            integer 	        опционально 	Номер страницы
    Пример: page[number]=2

    size 	            integer 	        опционально 	Количество элементов на странице
    Пример: page[size]=10

    ==============
    sort

    Название 	        Тип 	            Обязательность 	Описание
    field 	            string 	            опционально 	Поле сортировки [created_at/updated_at]
    Пример: sorting[field]=created_at

    direction 	        string 	            опционально 	Направление сортировки [reverse/forward]
    Пример: sorting[direction]=reverse
    """

    def __init__(
        self,
        company_ids: typing.Optional[typing.List[int]] = None,
        contact_ids: typing.Optional[typing.List[int]] = None,
        service_object_ids: typing.Optional[typing.List[int]] = None,
        status_codes: typing.Optional[typing.List[str]] = None,
        priority_codes: typing.Optional[typing.List[str]] = None,
        type_codes: typing.Optional[typing.List[str]] = None,
        created_since: typing.Optional[datetime.date] = None,
        created_until: typing.Optional[datetime.date] = None,
        completed_since: typing.Optional[datetime.date] = None,
        completed_until: typing.Optional[datetime.date] = None,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        sorting_field: typing.Optional[
            typing.Literal["created_at", "updated_at"]
        ] = None,
        sorting_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ):
        """

        :param company_ids: Array of company IDs to search for (Массив ID компаний, по которым осуществляется поиск)
        :param contact_ids: Array of contact IDs to search for (Массив ID контактов, по которым осуществляется поиск)
        :param service_object_ids: Array of service object IDs to search for (Массив ID объектов обслуживания, по которым осуществляется поиск)
        :param status_codes: Array of request status codes to search for (Массив Кодов статусов заявок, по которым осуществляется поиск)
        :param priority_codes: Array of request priority codes to search for (Массив Кодов приоритетов заявок, по которым осуществляется поиск)
        :param type_codes: Array of request type codes to search for (Массив Кодов типов заявок, по которым осуществляется поиск)
        :param created_since: Date of request creation (Since) (Дата создания заявки (С))
        :param created_until: Date of request creation (Until) (Дата создания заявки (По))
        :param completed_since: Date of request completion (Since) (Дата решения заявки (С))
        :param completed_until: Date of request completion (Until) (Дата решения заявки (По))
        :param page_number: Page number (Номер страницы)
        :param page_size: Number of elements per page (Количество элементов на странице)
        :param sorting_field: Sorting field (Поле сортировки)
        :param sorting_direction: Sorting direction (Направление сортировки)
        """
        self.company_ids: typing.Optional[typing.List[int]] = company_ids
        self.contact_ids: typing.Optional[typing.List[int]] = contact_ids
        self.service_object_ids: typing.Optional[typing.List[int]] = service_object_ids
        self.status_codes: typing.Optional[typing.List[str]] = status_codes
        self.priority_codes: typing.Optional[typing.List[str]] = priority_codes
        self.type_codes: typing.Optional[typing.List[str]] = type_codes
        self.created_since: typing.Optional[datetime.date] = created_since
        self.created_until: typing.Optional[datetime.date] = created_until
        self.completed_since: typing.Optional[datetime.date] = completed_since
        self.completed_until: typing.Optional[datetime.date] = completed_until

        self.page_number: typing.Optional[int] = page_number
        self.page_size: typing.Optional[int] = page_size

        self.sorting_field: typing.Optional[
            typing.Literal["created_at", "updated_at"]
        ] = sorting_field
        self.sorting_direction: typing.Optional[
            typing.Literal["reverse", "forward"]
        ] = sorting_direction

    def to_request(self) -> dict:
        params: typing.Dict[str, typing.Union[str, typing.List[str]]] = {}
        if self.company_ids is not None:
            params["company_ids"] = [str(company_id) for company_id in self.company_ids]
        if self.contact_ids is not None:
            params["contact_ids"] = [str(contact_id) for contact_id in self.contact_ids]
        if self.service_object_ids is not None:
            params["service_object_ids"] = [
                str(service_object_id) for service_object_id in self.service_object_ids
            ]
        if self.status_codes is not None:
            params["status_codes"] = [
                str(status_code) for status_code in self.status_codes
            ]
        if self.priority_codes is not None:
            params["priority_codes"] = [
                str(priority_code) for priority_code in self.priority_codes
            ]
        if self.type_codes is not None:
            params["type_codes"] = [str(type_code) for type_code in self.type_codes]
        if self.created_since is not None:
            params["created_since"] = self.created_since.strftime("%Y-%m-%d")
        if self.created_until is not None:
            params["created_until"] = self.created_until.strftime("%Y-%m-%d")
        if self.completed_since is not None:
            params["completed_since"] = self.completed_since.strftime("%Y-%m-%d")
        if self.completed_until is not None:
            params["completed_until"] = self.completed_until.strftime("%Y-%m-%d")

        if self.page_number is not None:
            params["page[number]"] = str(self.page_number)
        if self.page_size is not None:
            params["page[size]"] = str(self.page_size)

        if self.sorting_field is not None:
            params["sorting[field]"] = self.sorting_field
        if self.sorting_direction is not None:
            params["sorting[direction]"] = self.sorting_direction

        return {
            "method": "GET",
            "url": "api/v1/issues/list",
            "params": params,
        }

    def from_response(self, result) -> typing.List[Issue]:
        return [Issue.json_parse(issue) for issue in result]


class PostRatingIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!oczenka-zayavki-oczenka-zayavki

    POST /api/v1/issues/{issue_id}/rates

    Название 	Тип 	    Обязательность 	Описание
    rate 	    string 	    обязательный 	Оценка заявки
    Допустимые значения: bad - Плохо, normal - Нормально, good - Хорошо


    issue_id 	integer 	обязательный 	Идентификатор заявки
    """

    def __init__(
        self,
        issue_id: int,
        rate: typing.Literal["bad", "normal", "good"],
    ):
        """

        :param issue_id: Issue ID (Идентификатор заявки)
        :param rate: Issue rating (Оценка заявки)
        """
        self.issue_id: int = issue_id
        self.rate: typing.Literal["bad", "normal", "good"] = rate

    def to_request(self) -> dict:
        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/rates",
            "json": {
                "rate": self.rate,
            },
        }

    def from_response(self, result) -> dict:
        return result


class GetIssueSpecificationsRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-speczifikaczij-zayavki-poluchenie-speczifikaczij-zayavki

    GET /api/v1/issues/{issue_id}/services

    issue_id 	integer 	обязательный 	Идентификатор заявки
    """

    def __init__(
        self,
        issue_id: int,
    ):
        """

        :param issue_id: ID of issue (ID заявки)
        """
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/services",
        }

    def from_response(self, result) -> typing.List[Specification]:
        return [Specification.json_parse(issue_service) for issue_service in result]


class AddSpecificationToIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-speczifikaczij-zayavki-dobavlenie-speczifikaczii-k-zayavke

    POST /api/v1/issues/{issue_id}/services
    Название 	    Тип 	Обязательность 	Описание
    code 	        string 	обязательный 	Код строки спецификации из прайс-листа
    quantity 	    number 	обязательный 	Количество (неотрицательное число)
    performer_id 	integer опционально 	ID исполнителя
    price_list_id 	integer опционально 	ID прайс-листа
    comment 	    string 	опционально 	Комментарий
    total 	        number 	опционально 	Стоимость (неотрицательное число)
    discount 	    integer опционально 	Скидка (целое число от 0 до 100)

    p.s.: discount - float.


    issue_id 	    integer обязательный 	Идентификатор заявки
    """

    def __init__(
        self,
        issue_id: int,
        code: str,
        quantity: float,
        performer_id: typing.Optional[int] = None,
        price_list_id: typing.Optional[int] = None,
        comment: typing.Optional[str] = None,
        total: typing.Optional[float] = None,
        discount: typing.Optional[int] = None,
    ):
        """

        :param issue_id:  ID of issue (ID заявки)
        :param code: Code of specification (Код строки спецификации из прайс-листа)
        :param quantity: Quantity (Количество (неотрицательное число))
        :param performer_id: ID of performer (ID исполнителя)
        :param price_list_id: ID of price list (ID прайс-листа)
        :param comment: Comment (Комментарий)
        :param total: Total (Стоимость (неотрицательное число))
        :param discount: Discount (Скидка (целое число от 0 до 100))
        """
        self.issue_id: int = issue_id
        self.code: str = code
        self.quantity: float = quantity
        self.performer_id: typing.Optional[int] = performer_id
        self.price_list_id: typing.Optional[int] = price_list_id
        self.comment: typing.Optional[str] = comment
        self.total: typing.Optional[float] = total
        self.discount: typing.Optional[int] = discount

    def to_request(self) -> dict:
        json_data = {
            "code": self.code,
            "quantity": self.quantity,
        }
        if self.performer_id is not None:
            json_data["performer_id"] = self.performer_id
        if self.price_list_id is not None:
            json_data["price_list_id"] = self.price_list_id
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.total is not None:
            json_data["total"] = self.total
        if self.discount is not None:
            json_data["discount"] = self.discount

        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/services",
            "json": {"issue_service": {json_data}},
        }

    def from_response(self, result) -> Specification:
        return Specification.json_parse(result)


class GetTimeEntriesIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-detalizaczii-po-trudozatratam-zayavki-poluchenie-detalizaczii-po-trudozatratam-zayavki

    GET /api/v1/issues/{issue_id}/time_entries
    """

    def __init__(self, issue_id: int):
        """

        :param issue_id: ID of issue (ID заявки)
        """
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/time_entries",
        }

    def from_response(self, result) -> typing.List[TimeEntry]:
        return [TimeEntry.json_parse(item) for item in result]


class AddTimeEntryIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-detalizaczii-po-trudozatratam-zayavki-spisanie-trudozatrat-po-zayavke

    POST api/v1/issues/{issue_id}/time_entries

    Название 	            Тип 	            Обязательность 	Описание
    employee_id 	        integer 	        обязательный 	ID сотрудника, от имени которого списываются трудозатраты
    formatted_spent_time 	string 	            обязательный 	Количество списываемого времени(2 ч. 30 мин. или 2:30 или 2,5 часа и т.д.)
    logged_at 	            string 	            обязательный 	Дата списания
    comment 	            string 	            опционально 	Комментарий
    custom_parameters 	    associative array 	опционально 	Дополнительные атрибуты трудозатрат


    issue_id: int
    """

    def __init__(
        self,
        issue_id: int,
        employee_id: int,
        formatted_spent_time: str,
        logged_at: datetime.datetime,
        comment: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
    ):
        """

        :param issue_id: ID of issue (ID заявки)
        :param employee_id: ID of employee (ID сотрудника)
        :param formatted_spent_time: Formatted spent time (Количество списываемого времени)
        :param logged_at: Logged at (Дата списания)
        :param comment: Comment (Комментарий)
        :param custom_parameters: Custom parameters (Дополнительные атрибуты трудозатрат)
        """
        self.issue_id: int = issue_id
        self.employee_id: int = employee_id
        self.formatted_spent_time: str = formatted_spent_time
        self.logged_at: datetime.datetime = logged_at
        self.comment: typing.Optional[str] = comment
        self.custom_parameters: typing.Optional[dict] = custom_parameters

    def to_request(self) -> dict:
        json_data = {
            "employee_id": self.employee_id,
            "formatted_spent_time": self.formatted_spent_time,
            "logged_at": self.logged_at.strftime("%Y-%m-%d %H:%M"),
        }
        if self.comment is not None:
            json_data["comment"] = self.comment
        if self.custom_parameters is not None:
            json_data["custom_parameters"] = self.custom_parameters

        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/time_entries",
            "json": {"time_entries": [json_data]},
        }

    def from_response(self, result) -> TimeEntry:
        return TimeEntry.json_parse(result)


class GetIssueFileRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-spiska-fajlov-zayavki-poluchenie-spiska-fajlov-zayavki

    GET /api/v1/issues/{issue_id}/attachments/{attachment_id}


    Обратите внимание

    Размер файла (attachment_file_size) измеряется в байтах. Ссылка на файл заявки временная: она работает в течение
    30 секунд после создания.

    """

    def __init__(self, issue_id: int, attachment_id: int):
        """

        :param issue_id: ID of issue (ID заявки)
        :param attachment_id: ID of attachment (ID вложения)
        """
        self.issue_id: int = issue_id
        self.attachment_id: int = attachment_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/attachments/{self.attachment_id}",
        }

    def from_response(self, result) -> shared.Attachment:
        return shared.Attachment.json_parse(result)


class GetIssueCheckListRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-chek-lista-zayavki-poluchenie-chek-lista-zayavki

    GET /api/v1/issues/{issue_id}/check_lists/items

    """

    def __init__(self, issue_id: int):
        """

        :param issue_id: ID of issue (ID заявки)
        """
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}/check_lists/items",
        }

    def from_response(self, result) -> typing.List[CheckListItem]:
        return [CheckListItem.json_parse(item) for item in result]


class AddIssueCheckListItemRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!poluchenie-chek-lista-zayavki-sozdanie-chek-lista-zayavki

    POST /api/v1/issues/{issue_id}/check_lists/items

    Ограничения для передаваемых параметров ¶

        Нельзя передавать заголовки на 3 и более уровне вложенности.

        Максимальное количество создаваемых пунктов и заголовков - 200.


    """

    class CheckListAdd:
        """
        Название 	                    Тип 	            Обязательность 	Описание
        name 	                        string 	            обязательный 	Название пункта чек-листа.
        item_type 	                    string 	            обязательный 	Тип пункта чек-листа. Может принимать значение point (пункт) или header (заголовок).
        required_to_status_codes 	    array of string 	опционально 	Массив кодов статусов, при входе в которые пункт обязателен к выполнению. Передается только для обязательных пунктов чек-листа.
        required_from_status_codes 	    array of string 	опционально 	Массив кодов статусов, при выходе из которых пункт обязателен к выполнению. Передается только для обязательных пунктов чек-листа.
        visible_for_clients 	        boolean 	        опционально 	Видимость для клиента.
        planned_execution_in_minutes 	number 	            опционально 	Плановая продолжительность (в минутах)
        parameters 	                    associative array 	опционально 	Параметры строки чек-листа. Может содержать ключи files (параметр выполнения “Фото”), text (параметр выполнения “Комментарий”) и string (параметр выполнения “Строка”), для которых допустимы значения required (обязательный) и unrequired (необязательный).
        children 	                    array 	            опционально 	Вложенные пункты чек-листа. Передается только для пунктов чек-листа с типом header.
        """

        def __init__(
            self,
            name: str,
            item_type: typing.Literal["point", "header"],
            required_to_status_codes: typing.List[str] = None,
            required_from_status_codes: typing.List[str] = None,
            visible_for_clients: bool = None,
            planned_execution_in_minutes: int = None,
            parameters: dict = None,
            children: typing.List["AddIssueCheckListItemRequest.CheckListAdd"] = None,
        ):
            self.name = name
            self.item_type = item_type
            self.required_to_status_codes = required_to_status_codes
            self.required_from_status_codes = required_from_status_codes
            self.visible_for_clients = visible_for_clients
            self.planned_execution_in_minutes = planned_execution_in_minutes
            self.parameters = parameters
            self.children = children

        def to_json(self):
            return {
                "name": self.name,
                "item_type": self.item_type,
                "required_to_status_codes": self.required_to_status_codes,
                "required_from_status_codes": self.required_from_status_codes,
                "visible_for_clients": self.visible_for_clients,
                "planned_execution_in_minutes": self.planned_execution_in_minutes,
                "parameters": self.parameters,
                "children": [child.to_json() for child in self.children],
            }

    def __init__(
        self,
        issue_id: int,
        check_list: typing.List[CheckListAdd],
    ):
        """

        :param issue_id: ID of issue (ID заявки)
        :param check_list: Check list (Чек-лист)
        """
        self.issue_id: int = issue_id
        self.check_list: typing.List[
            AddIssueCheckListItemRequest.CheckListAdd
        ] = check_list

    def to_request(self) -> dict:

        return {
            "method": "POST",
            "url": f"api/v1/issues/{self.issue_id}/check_lists/items",
            "json": {
                "check_list": {"items": [item.to_json() for item in self.check_list]}
            },
        }

    def from_response(self, result) -> typing.List[CheckListItem]:
        return [
            CheckListItem.json_parse(item) for item in result["check_list"]["items"]
        ]


class MarkCheckedChecklistItemIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!pometka-o-vypolnenii-stroki-chek-lista-pometka-o-vypolnenii-stroki-chek-lista

    PATCH /api/v1/issues/{issue_id}/check_lists/items/{item_id}/check

    Название 	        Тип 	            Обязательность 	Описание
    checked 	        boolean 	        обязательный 	Признак выполненности
    item_parameters 	associative array 	опционально 	Параметры строки чек-листа


    Название 	Тип 	Обязательность 	Описание
    attachment 	string 	обязательный 	Прикрепляемый файл

    """

    def __init__(
        self,
        issue_id: int,
        item_id: int,
        checked: bool,
        item_parameters: dict = None,
        attachment: str = None,
    ):
        """

        :param issue_id: ID of issue (ID заявки)
        :param item_id: ID of checklist item (ID строки чек-листа)
        :param checked: Checked (Признак выполненности)
        :param item_parameters: Item parameters (Параметры строки чек-листа)
        :param attachment: Attachment (Прикрепляемый файл)
        """
        self.issue_id: int = issue_id
        self.item_id: int = item_id
        self.checked: bool = checked
        self.item_parameters: dict = item_parameters
        self.attachment: str = attachment

    def to_request(self) -> dict:
        if self.attachment is None:
            json_data = {
                "checked": self.checked,
            }
            if self.item_parameters is not None:
                json_data["item_parameters"] = self.item_parameters
            return {
                "method": "PATCH",
                "url": f"api/v1/issues/{self.issue_id}/check_lists/items/{self.item_id}/check",
                "json": {"check_list_item": json_data},
            }
        else:
            multipart_data = MultipartEncoder({})
            multipart_data.fields["check_list_item[checked]"] = str(
                self.checked
            ).lower()
            if self.item_parameters is not None:
                for key, value in self.item_parameters.items():
                    multipart_data.fields[
                        f"check_list_item[item_parameters][{key}]"
                    ] = value
            multipart_data.fields[
                "check_list_item[item_parameters][files][0][attachment]"
            ] = (
                os.path.basename(self.attachment),
                open(self.attachment, "rb"),
                mimetypes.guess_type(self.attachment)[0],
            )
            return {
                "method": "PATCH",
                "url": f"api/v1/issues/{self.issue_id}/check_lists/items/{self.item_id}/check",
                "data": multipart_data.read(),
                "headers": {
                    "Content-Type": multipart_data.content_type,
                },
            }

    def from_response(self, result) -> typing.List[CheckListItem]:
        return [CheckListItem.json_parse(check_list_item) for check_list_item in result]


class GetIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!informacziya-o-zayavke-informacziya-o-zayavke

    GET /api/v1/issues/{issue_id}

    Название 	Тип 	Обязательность 	Описание
    issue_id 	integer 	обязательный 	ID заявки

    """

    def __init__(self, issue_id: int):
        """

        :param issue_id: Id of the issue (ID заявки)
        """
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "GET",
            "url": f"api/v1/issues/{self.issue_id}",
        }

    def from_response(self, result) -> Issue:
        return Issue.json_parse(result)


class DeleteIssueRequest(types.ApiRequest):
    """
    https://okdesk.ru/apidoc#!informacziya-o-zayavke-udalenie-zayavki

    DELETE /api/v1/issues/{issue_id}

    Название 	Тип 	Обязательность 	Описание
    issue_id 	integer 	обязательный 	ID заявки

    """

    def __init__(self, issue_id: int):
        self.issue_id: int = issue_id

    def to_request(self) -> dict:
        return {
            "method": "DELETE",
            "url": f"api/v1/issues/{self.issue_id}",
        }

    def from_response(self, result) -> None:
        return None
