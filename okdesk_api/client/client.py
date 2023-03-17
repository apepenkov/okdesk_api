import json
import typing

import aiohttp

from .. import types
from ..errors import OkDeskError
from ..api import (
    companies,
    issues,
    maintenance_entities,
    shared,
    equipments,
    references,
    price_lists,
)
from .. import helpers
import datetime


class OkDeskClient:
    def __init__(
        self,
        base_url: str,
        api_token: str,
        debug: bool = False,
    ):
        """
        Create a OkDesk instance.
        (Создает экземпляр OkDesk.)

        :param base_url:  Base URL for the OkDesk API (Базовый URL для API OkDesk) (https://<account>.okdesk.ru/api/v1/)
        :param api_token:  api_token (Токен)
        :param debug:  If True, prints all requests and responses (Если True, печатает все запросы и ответы)
        """
        import re

        if not base_url.endswith("/"):
            base_url += "/"
        if not re.match(r"https?://.*\.okdesk\.ru/$", base_url):
            raise ValueError(
                "base_url must be in the format https://<account>.okdesk.ru/"
            )
        self._base_url = base_url
        self._api_token = api_token
        self._debug = debug

    async def request(
        self,
        method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        allow_non_json=False,
        **kwargs,
    ) -> dict:
        """
        Make a request to the OkDesk API, automatically adding the Authorization pararm.
        (Делает запрос к API OkDesk, автоматически добавляя параметр Authorization.)

        :raises OkDeskError: if the request failed (Сообщает об ошибке, если запрос не удался)

        :param method: HTTP method GET, POST, PUT, DELETE
        :param url:  URL to request WITHOUT https://<account>.okdesk.ru/ (URL для запроса БЕЗ https://<account>.okdesk.ru/)
        :param allow_non_json:  If True, error is not raised if the response is not JSON (Если True, ошибка не вызывается, если ответ не JSON)
        :param kwargs:  Additional arguments for aiohttp.ClientSession.request
         (Дополнительные аргументы для aiohttp.ClientSession.request)

        :return: JSON Response from the OkDesk API (JSON ответ от API OkDesk)
        """
        if url.startswith("https://"):
            raise ValueError("url must not start with https://!")
        if url.startswith("/"):
            url = url[1:]
        url = self._base_url + url
        async with aiohttp.ClientSession() as session:
            kwargs.setdefault("params", {})
            kwargs.setdefault("headers", {})

            kwargs["params"]["api_token"] = self._api_token
            is_json = kwargs.get("json") is not None
            if is_json:
                kwargs["data"] = json.dumps(
                    kwargs.pop("json"),
                    separators=(",", ":"),
                    ensure_ascii=False,
                    indent=4 if self._debug else None,
                )
                kwargs["headers"]["Content-Type"] = "application/json"

            # allow gzipped responses
            # (разрешаем сжатые ответы)
            kwargs["headers"]["Accept-Encoding"] = "gzip"

            async with session.request(method, url, **kwargs) as resp:
                if self._debug:
                    to_print = f"Request: {method} {url}"
                    params_r = kwargs.get("params").copy()
                    params_r.pop("api_token")  # we don't want to print api_token
                    if params_r:
                        to_print += f"\nParams: {params_r}"
                    data_r = kwargs.get("data")
                    if data_r:
                        to_print += f"\nData: {data_r}"
                    to_print += (
                        f"\nResponse: {resp.status} {resp.reason} {resp.content_type}"
                    )
                    to_print += f"\nContent: {await resp.text()}"
                    print(to_print)

                if resp.content_type != "application/json":
                    if allow_non_json:
                        return {}
                    raise ValueError(
                        f"Response is not JSON: `{resp.content_type}` : {await resp.text()}"
                    )
                json_resp = await resp.json()
                if resp.status >= 400:
                    raise OkDeskError(json_resp["errors"])
                return json_resp

    # function that allows us to use client as a caller
    # (функция, которая позволяет нам использовать client как вызывающий)
    async def __call__(self, request):
        if not isinstance(request, types.ApiRequest):
            raise TypeError("request must be an ApiRequest")
        result = await self.request(**request.to_request())
        return request.from_response(result)

    # companies
    async def find_companies(
        self,
        name: typing.Optional[str] = None,
        phone: typing.Optional[str] = None,
        id_: typing.Optional[int] = None,
        crm_1c_id: typing.Optional[str] = None,
        search_string: typing.Optional[str] = None,
    ) -> typing.Optional[companies.Company]:
        """
        Поиск осуществляется по точному совпадению названия или дополнительного названия компании,
        телефона, внутреннего ID, идентификатора объекта в 1С или по подстроке

        При передаче параметра search_string остальные параметры не учитываются

        :param name: Имя компании
        :param phone: Телефон компании
        :param id_: Внутренний ID компании
        :param crm_1c_id: ID компании в 1С
        :param search_string: Искомая подстрока
        :return: Список компаний
        """
        return await self(
            companies.FindCompanyRequest(
                name=name,
                phone=phone,
                id_=id_,
                crm_1c_id=crm_1c_id,
                search_string=search_string,
            )
        )

    async def create_company(
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
    ) -> companies.Company:
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
        :return: Created company
        """

        return await self(
            companies.CreateCompanyRequest(
                name=name,
                additional_name=additional_name,
                site=site,
                email=email,
                phone=phone,
                address=address,
                coordinates=coordinates,
                comment=comment,
                observer_ids=observer_ids,
                default_assignee_id=default_assignee_id,
                category_code=category_code,
                crm_1c_id=crm_1c_id,
                custom_parameters=custom_parameters,
            )
        )

    async def update_company(
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
    ) -> companies.Company:
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
        :return: Updated company
        """

        return await self(
            companies.UpdateCompanyRequest(
                company_id=company_id,
                name=name,
                additional_name=additional_name,
                site=site,
                email=email,
                phone=phone,
                address=address,
                coordinates=coordinates,
                comment=comment,
                observer_ids=observer_ids,
                default_assignee_id=default_assignee_id,
                category_code=category_code,
                crm_1c_id=crm_1c_id,
                custom_parameters=custom_parameters,
            )
        )

    async def get_company_list(
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
    ) -> typing.List[companies.Company]:
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
        :return: List of companies
        """
        return await self(
            companies.GetCompanyListRequest(
                category_ids=category_ids,
                default_assignee_ids=default_assignee_ids,
                default_assignee_group_ids=default_assignee_group_ids,
                observer_ids=observer_ids,
                observer_group_ids=observer_group_ids,
                created_since=created_since,
                created_until=created_until,
                custom_parameters=custom_parameters,
                name=name,
                additional_name=additional_name,
                crm_1c_id=crm_1c_id,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    async def get_company_file(
        self, company_id: int, attachment_id: int
    ) -> shared.Attachment:
        """

        :param company_id: Company ID (ID компании)
        :param attachment_id:  Attachment ID (ID вложения)
        :return: Attachment
        """
        return await self(
            companies.GetCompanyFileRequest(
                company_id=company_id, attachment_id=attachment_id
            )
        )

    async def archive_company(self, company_id: int) -> companies.Company:
        """

        :param company_id: Company ID (ID компании)
        :return: Company
        """
        return await self(companies.ArchiveCompanyRequest(company_id=company_id))

    # maintenance entities
    async def create_maintenance_entity(
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
    ) -> maintenance_entities.MaintanceEntity:
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
        :return: Maintenance entity
        """
        return await self(
            maintenance_entities.CreateMaintenanceEntityRequest(
                name=name,
                company_id=company_id,
                agreement_ids=agreement_ids,
                address=address,
                coordinates=coordinates,
                timezone=timezone,
                comment=comment,
                default_assignee_id=default_assignee_id,
                default_assignee_group_id=default_assignee_group_id,
                schedule_id=schedule_id,
                observer_ids=observer_ids,
                observer_group_ids=observer_group_ids,
                custom_parameters=custom_parameters,
            )
        )

    async def search_maintenance_entities(
        self,
        name: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        search_string: typing.Optional[str] = None,
    ) -> typing.List[maintenance_entities.MaintanceEntity]:
        """

        :param name: Name of the service object (Название объекта обслуживания)
        :param comment: Additional information about the service object (Дополнительная информация об объекте обслуживания)
        :param search_string: Searched substring (Искомая подстрока)
        :return: Array of service objects (Массив объектов обслуживания)
        """
        return await self(
            maintenance_entities.SearchMaintenanceEntityRequest(
                name=name,
                comment=comment,
                search_string=search_string,
            )
        )

    async def update_maintenance_entity(
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
    ) -> maintenance_entities.MaintanceEntity:
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
        :return: Maintenance entity (Объект обслуживания)
        """

        return await self(
            maintenance_entities.UpdateMaintenanceEntityRequest(
                id_=id_,
                name=name,
                company_id=company_id,
                agreement_ids=agreement_ids,
                address=address,
                coordinates=coordinates,
                timezone=timezone,
                comment=comment,
                default_assignee_id=default_assignee_id,
                default_assignee_group_id=default_assignee_group_id,
                schedule_id=schedule_id,
                observer_ids=observer_ids,
                observer_group_ids=observer_group_ids,
                custom_parameters=custom_parameters,
            )
        )

    async def get_maintenance_entity(
        self, id_: int
    ) -> maintenance_entities.MaintanceEntity:
        """

        :param id_: Id (Идентификатор объекта обслуживания)
        :return: Maintenance entity (Объект обслуживания)
        """
        return await self(maintenance_entities.GetMaintenanceEntityRequest(id_=id_))

    async def list_maintenance_entities(
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
    ) -> typing.List[maintenance_entities.MaintanceEntity]:
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
        :return: Maintenance entities (Объекты обслуживания)
        """

        return await self(
            maintenance_entities.ListMaintenanceEntitiesRequest(
                company_ids=company_ids,
                default_assignee_ids=default_assignee_ids,
                default_assignee_group_ids=default_assignee_group_ids,
                created_since=created_since,
                created_until=created_until,
                updated_since=updated_since,
                updated_until=updated_until,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    async def add_maintenance_entity_attachment(
        self, maintenance_entity_id: int, attachments: typing.List[types.Attachment]
    ) -> maintenance_entities.MaintanceEntity:
        """

        :param maintenance_entity_id: Maintenance entity ID (ID объекта обслуживания)
        :param attachments:  (Список приложенных локальных файлов)
        :return: Maintenance entity (Объект обслуживания)
        """
        return await self(
            maintenance_entities.AddMaintenanceEntityAttachmentRequest(
                maintenance_entity_id=maintenance_entity_id,
                attachments=attachments,
            )
        )

    # issues
    async def create_issue(
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
    ) -> issues.Issue:
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
        :return: Created issue (Созданная заявка)
        """
        return await self(
            issues.CreateIssueRequest(
                title=title,
                description=description,
                company_id=company_id,
                contact_id=contact_id,
                agreement_id=agreement_id,
                assignee_id=assignee_id,
                group_id=group_id,
                observer_ids=observer_ids,
                observer_group_ids=observer_group_ids,
                contact_observer_ids=contact_observer_ids,
                maintenance_entity_id=maintenance_entity_id,
                equipment_ids=equipment_ids,
                type_=type_,
                priority=priority,
                deadline_at=deadline_at,
                start_execution_until=start_execution_until,
                planned_execution_in_minutes=planned_execution_in_minutes,
                custom_parameters=custom_parameters,
                parent_id=parent_id,
                author=author,
                files=files,
            )
        )

    async def change_issue_assignee(
        self,
        issue_id: int,
        assignee_id: typing.Optional[int] = None,
        group_id: typing.Optional[int] = None,
    ) -> issues.Issue:
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param assignee_id: ID of the assignee (optional) (ID ответственного за заявку)
        :param group_id: ID of the group (optional) (ID ответственной группы)
        """
        return await self(
            issues.ChangeIssueAssigneeRequest(
                issue_id=issue_id,
                assignee_id=assignee_id,
                group_id=group_id,
            )
        )

    async def change_issue_deadline(
        self,
        issue_id: int,
        deadline_at: typing.Optional[datetime.datetime] = None,
    ) -> issues.Issue:
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param deadline_at: deadline of the issue (optional) (Срок выполнения заявки)
        :return: Changed issue (Измененная заявка)
        """
        return await self(
            issues.ChangeIssueDeadlineRequest(
                issue_id=issue_id,
                deadline_at=deadline_at,
            )
        )

    async def change_issue_code(
        self,
        issue_id: int,
        code: str,
    ) -> issues.Issue:
        """

        :param issue_id: ID of the issue   (ID заявки )
        :param code: Code of the issue type (Код типа заявки)
        :return: Changed issue (Измененная заявка)
        """
        return await self(
            issues.ChangeIssueCodeRequest(
                issue_id=issue_id,
                code=code,
            )
        )

    async def change_issue_parameters(
        self,
        issue_id: int,
        custom_parameters: typing.Dict[str, typing.Any],
    ) -> None:
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param custom_parameters:  Custom parameters of the issue (Объект с параметрами заявки)
        :return: Changed issue (Измененная заявка)
        """

        return await self(
            issues.ChangeIssueParametersRequest(
                issue_id=issue_id,
                custom_parameters=custom_parameters,
            )
        )

    async def change_issue_address(
        self,
        issue_id: int,
        value: str,
        coordinates: typing.List[float],
    ) -> issues.Issue:
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param value:  String representation of the issue address (Строковое представление адреса заявки)
        :param coordinates:  Coordinates of the issue address (Координаты адреса заявки)
        :return: Changed issue (Измененная заявка)
        """
        return await self(
            issues.ChangeIssueAddressRequest(
                issue_id=issue_id,
                value=value,
                coordinates=coordinates,
            )
        )

    async def change_issue_status(
        self,
        issue_id: int,
        code: str,
        delay_to: typing.Optional[datetime.datetime] = None,
        comment: typing.Optional[str] = None,
        comment_public: typing.Optional[bool] = None,
        custom_parameters: typing.Optional[dict] = None,
        time_entry: typing.Optional[list] = None,
        skip_options: typing.Optional[list] = None,
    ) -> issues.Issue:
        """

        :param issue_id: ID of the issue (required) (ID заявки (обязательно))
        :param code: Code of the status (required) (Код статуса (обязательно))
        :param delay_to: Time, until which the application is postponed. Required only for the delayed status. For the rest of the statuses, this parameter will be ignored. (Время, до которого откладывается заявка. Обязательное поле только для статуса delayed. Для остальных статусов данный параметр будет игнорироваться.)
        :param comment: Comment to the status. For example, the reason for the transition to a new status. The necessity of this parameter is configured in the section “Settings / Tickets / Ticket Statuses”. (Комментарий к статусу. Например, причина перехода в новый статус. Обязательность данного параметра настраивается в разделе “Настройки/Заявки/Статусы заявок”.)
        :param comment_public: Flag of the publicness of the comment. Takes the value true or false (Флаг публичности комментария. Принимает значение true или false)
        :param custom_parameters: Additional attributes of the application that the user can fill in when entering a new or exiting the current status. (Дополнительные атрибуты заявки, которые доступны пользователю для заполнения при входе в новый или при выходе из текущего статуса.)
        :param time_entry: Array of time entries for the application that will be added when changing the status (Массив трудозатрат по заявке, которые будут добавлены при смене статуса)
        :param skip_options: Array of flags that allow you to skip sending notifications (skip_notifications), webhooks (skip_webhooks), automatic actions (skip_triggers) (Массив флагов, позволяющих пропустить отправку оповещений (skip_notifications), вебхуков (skip_webhooks), автоматических действий (skip_triggers))
        :return: Changed issue (Измененная заявка)
        """
        return await self(
            issues.ChangeIssueStatusRequest(
                issue_id=issue_id,
                code=code,
                delay_to=delay_to,
                comment=comment,
                comment_public=comment_public,
                custom_parameters=custom_parameters,
                time_entry=time_entry,
                skip_options=skip_options,
            )
        )

    async def issue_add_comment(
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
        :param attachments: List of attached files (Список приложенных локальных файлов)
        :return: Added comment (Добавленный комментарий)
        """
        return await self(
            issues.AddCommentRequest(
                issue_id=issue_id,
                content=content,
                author_id=author_id,
                author_type=author_type,
                public=public,
                attachments=attachments,
            )
        )

    async def get_issue_comments(self, issue_id: int) -> typing.List[issues.Comment]:
        """

        :param issue_id: Issue ID (ID обращения)
        :return: List of comments (Список комментариев)
        """
        return await self(issues.GetCommentsRequest(issue_id=issue_id))

    async def get_issues_id_list(
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
    ) -> typing.List[int]:
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
        :return:
        """
        return await self(
            issues.GetIssuesListIdRequest(
                assignee_ids=assignee_ids,
                assignee_group_ids=assignee_group_ids,
                company_ids=company_ids,
                agreement_ids=agreement_ids,
                contact_ids=contact_ids,
                author_employee_ids=author_employee_ids,
                author_contact_ids=author_contact_ids,
                maintenance_entity_ids=maintenance_entity_ids,
                equipment_ids=equipment_ids,
                status=status,
                status_not=status_not,
                opened=opened,
                priority=priority,
                type_=type_,
                rate=rate,
                created_since=created_since,
                created_until=created_until,
                overdue=overdue,
                overdue_reaction=overdue_reaction,
                completed_since=completed_since,
                completed_until=completed_until,
                updated_since=updated_since,
                updated_until=updated_until,
                reacted_since=reacted_since,
                reacted_until=reacted_until,
                deadline_since=deadline_since,
                deadline_until=deadline_until,
                start_execution_since=start_execution_since,
                start_execution_until=start_execution_until,
                planned_reaction_since=planned_reaction_since,
                planned_reaction_until=planned_reaction_until,
                custom_parameters=custom_parameters,
            )
        )

    async def get_issues_list_rich(
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
    ) -> typing.List[issues.Issue]:
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
        :return: Found issues (Найденные заявки)
        """
        return await self(
            issues.GetIssuesListRichRequest(
                company_ids=company_ids,
                contact_ids=contact_ids,
                service_object_ids=service_object_ids,
                status_codes=status_codes,
                priority_codes=priority_codes,
                type_codes=type_codes,
                created_since=created_since,
                created_until=created_until,
                completed_since=completed_since,
                completed_until=completed_until,
                page_number=page_number,
                page_size=page_size,
                sorting_field=sorting_field,
                sorting_direction=sorting_direction,
            )
        )

    async def post_issue_rating(
        self,
        issue_id: int,
        rate: typing.Literal["bad", "normal", "good"],
    ) -> dict:
        """

        :param issue_id: Issue ID (Идентификатор заявки)
        :param rate: Issue rating (Оценка заявки)
        :return: Result (Результат)
        """
        return await self(
            issues.PostRatingIssueRequest(
                issue_id=issue_id,
                rate=rate,
            )
        )

    async def get_issue_specifications(
        self,
        issue_id: int,
    ) -> typing.List[issues.Specification]:
        """

        :param issue_id: ID of issue (ID заявки)
        :return: Specifications (Спецификации)
        """
        return await self(
            issues.GetIssueSpecificationsRequest(
                issue_id=issue_id,
            )
        )

    async def add_specification_to_issue(
        self,
        issue_id: int,
        code: str,
        quantity: float,
        performer_id: typing.Optional[int] = None,
        price_list_id: typing.Optional[int] = None,
        comment: typing.Optional[str] = None,
        total: typing.Optional[float] = None,
        discount: typing.Optional[int] = None,
    ) -> issues.Specification:
        """

        :param issue_id:  ID of issue (ID заявки)
        :param code: Code of specification (Код строки спецификации из прайс-листа)
        :param quantity: Quantity (Количество (неотрицательное число))
        :param performer_id: ID of performer (ID исполнителя)
        :param price_list_id: ID of price list (ID прайс-листа)
        :param comment: Comment (Комментарий)
        :param total: Total (Стоимость (неотрицательное число))
        :param discount: Discount (Скидка (целое число от 0 до 100))
        :return: Specification (Спецификация)
        """

        return await self(
            issues.AddSpecificationToIssueRequest(
                issue_id=issue_id,
                code=code,
                quantity=quantity,
                performer_id=performer_id,
                price_list_id=price_list_id,
                comment=comment,
                total=total,
                discount=discount,
            )
        )

    async def get_time_entries_issue(
        self, issue_id: int
    ) -> typing.List[issues.TimeEntry]:
        """

        :param issue_id: ID of issue (ID заявки)
        :return: Time entries (Записи времени)
        """
        return await self(
            issues.GetTimeEntriesIssueRequest(
                issue_id=issue_id,
            )
        )

    async def add_time_entry_issue(
        self,
        issue_id: int,
        employee_id: int,
        formatted_spent_time: str,
        logged_at: datetime.datetime,
        comment: typing.Optional[str] = None,
        custom_parameters: typing.Optional[dict] = None,
    ) -> issues.TimeEntry:
        """

        :param issue_id: ID of issue (ID заявки)
        :param employee_id: ID of employee (ID сотрудника)
        :param formatted_spent_time: Formatted spent time (Количество списываемого времени)
        :param logged_at: Logged at (Дата списания)
        :param comment: Comment (Комментарий)
        :param custom_parameters: Custom parameters (Дополнительные атрибуты трудозатрат)
        :return: Created Time entry (Созданная запись времени)
        """
        return await self(
            issues.AddTimeEntryIssueRequest(
                issue_id=issue_id,
                employee_id=employee_id,
                formatted_spent_time=formatted_spent_time,
                logged_at=logged_at,
                comment=comment,
                custom_parameters=custom_parameters,
            )
        )

    async def get_file_of_issue(
        self, issue_id: int, attachment_id: int
    ) -> shared.Attachment:
        """

        :param issue_id: ID of issue (ID заявки)
        :param attachment_id: ID of attachment (ID вложения)
        :return: Attachment (Вложение)
        """
        return await self(
            issues.GetIssueFileRequest(
                issue_id=issue_id,
                attachment_id=attachment_id,
            )
        )

    async def get_issue_checklist(
        self, issue_id: int
    ) -> typing.List[issues.CheckListItem]:
        """

        :param issue_id: ID of issue (ID заявки)
        """

        return await self(
            issues.GetIssueCheckListRequest(
                issue_id=issue_id,
            )
        )

    async def add_issue_checklist(
        self,
        issue_id: int,
        check_list: typing.List[issues.AddIssueCheckListItemRequest.CheckListAdd],
    ) -> typing.List[issues.CheckListItem]:
        """

        :param issue_id: ID of issue (ID заявки)
        :param check_list: Check list (Чек-лист)
        :return: Check list (Чек-лист)
        """
        return await self(
            issues.AddIssueCheckListItemRequest(
                issue_id=issue_id,
                check_list=check_list,
            )
        )

    async def mark_checked_checklist_item_issue(
        self,
        issue_id: int,
        item_id: int,
        checked: bool,
        item_parameters: dict = None,
        attachment: str = None,
    ) -> typing.List[issues.CheckListItem]:
        """

        :param issue_id: ID of issue (ID заявки)
        :param item_id: ID of checklist item (ID строки чек-листа)
        :param checked: Checked (Признак выполненности)
        :param item_parameters: Item parameters (Параметры строки чек-листа)
        :param attachment: Attachment (Прикрепляемый файл)
        :return: Check list (Чек-лист)
        """
        return await self(
            issues.MarkCheckedChecklistItemIssueRequest(
                issue_id=issue_id,
                item_id=item_id,
                checked=checked,
                item_parameters=item_parameters,
                attachment=attachment,
            )
        )

    async def get_issue(self, issue_id: int) -> issues.Issue:
        """

        :param issue_id: ID of issue (ID заявки)
        :return: Issue (Заявка)
        """
        return await self(
            issues.GetIssueRequest(
                issue_id=issue_id,
            )
        )

    async def delete_issue(self, issue_id: int) -> None:
        """

        :param issue_id: ID of issue (ID заявки)
        """
        return await self(
            issues.DeleteIssueRequest(
                issue_id=issue_id,
            )
        )

    # equipments
    async def find_equipment(
        self,
        inventory_number: str = None,
        serial_number: str = None,
        search_string: str = None,
    ) -> typing.Optional[equipments.Equipment]:
        """

        :param inventory_number: Inventory number of equipment (Инвентарный номер оборудования)
        :param serial_number: Serial number of equipment (Серийный номер оборудования)
        :param search_string: Search string (Искомая подстрока)
        :return: Equipment (Оборудование)
        """
        return await self(
            equipments.FindEquipmentRequest(
                inventory_number=inventory_number,
                serial_number=serial_number,
                search_string=search_string,
            )
        )

    async def create_equipment(
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
    ) -> equipments.Equipment:
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
        :return: Equipment (Оборудование)
        """
        return await self(
            equipments.CreateEquipmentRequest(
                equipment_type_code=equipment_type_code,
                equipment_manufacturer_code=equipment_manufacturer_code,
                equipment_model_code=equipment_model_code,
                serial_number=serial_number,
                inventory_number=inventory_number,
                comment=comment,
                company_id=company_id,
                maintenance_entity_id=maintenance_entity_id,
                parent_id=parent_id,
                custom_parameters=custom_parameters,
                agreement_ids=agreement_ids,
            )
        )

    async def update_equipment(
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
    ) -> equipments.Equipment:
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
        :return: Equipment (Оборудование)
        """
        return await self(
            equipments.UpdateEquipmentRequest(
                equipment_id=equipment_id,
                equipment_type_code=equipment_type_code,
                equipment_manufacturer_code=equipment_manufacturer_code,
                equipment_model_code=equipment_model_code,
                serial_number=serial_number,
                inventory_number=inventory_number,
                comment=comment,
                company_id=company_id,
                maintenance_entity_id=maintenance_entity_id,
                parent_id=parent_id,
                custom_parameters=custom_parameters,
                agreement_ids=agreement_ids,
            )
        )

    async def get_equipment(self, equipment_id: int) -> equipments.Equipment:
        """

        :param equipment_id: ID of equipment (ID оборудования)
        :return: Equipment (Оборудование)
        """
        return await self(equipments.GetEquipmentRequest(equipment_id=equipment_id))

    async def get_equipment_list(
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
    ) -> typing.List[equipments.Equipment]:
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
        :return: Array of equipment (Массив оборудования)
        """
        return await self(
            equipments.ListEquipmentsRequest(
                company_ids=company_ids,
                maintenance_entity_ids=maintenance_entity_ids,
                agreement_ids=agreement_ids,
                created_since=created_since,
                created_until=created_until,
                equipment_kind_codes=equipment_kind_codes,
                equipment_manufacturer_codes=equipment_manufacturer_codes,
                equipment_model_codes=equipment_model_codes,
                custom_parameters=custom_parameters,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    # references

    async def get_equipment_manufacturers(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[references.EquipmentManufacturer]:

        """

        :param search_string: String with search query (Строка с поисковым запросом)
        :param page_size: Number of returned records. Cannot exceed 100. (Количество возвращаемых записей. Не может превышать 100.)
        :param page_from_id: ID of the manufacturer of the equipment from which the selection of records begins. (ID производителя оборудования, с которого начинается выборка записей.)
        :param page_direction: Selection direction. (Направление выборки.)
        :return: Array of equipment manufacturers (Массив производителей оборудования)
        """
        return await self(
            references.GetManufacturersRequest(
                search_string=search_string,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    async def create_equipment_manufacturer(
        self,
        name: str,
        code: str,
        description: typing.Optional[str] = None,
    ) -> references.EquipmentManufacturer:

        """

        :param name: Name of the manufacturer of the equipment (Название производителя оборудования)
        :param code: Manufacturer code (Код производителя оборудования)
        :param description: Manufacturer description (Описание производителя оборудования)
        :return: Manufacturer of the equipment (Производитель оборудования)
        """
        return await self(
            references.CreateManufacturerRequest(
                name=name,
                code=code,
                description=description,
            )
        )

    async def update_equipment_manufacturer(
        self,
        manufacturer_id: int,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
    ) -> references.EquipmentManufacturer:
        """
        Update equipment manufacturer (Обновить производителя оборудования)

        :param manufacturer_id: Manufacturer ID (ID производителя оборудования)
        :param name: Name of the manufacturer of the equipment (Название производителя оборудования)
        :param description: Manufacturer description (Описание производителя оборудования)
        :param visible: Manufacturer visibility (Признак включенности)
        :return: Updated manufacturer of the equipment (Обновленный производитель оборудования)
        """

        return await self(
            references.UpdateManufacturerRequest(
                manufacturer_id=manufacturer_id,
                name=name,
                description=description,
                visible=visible,
            )
        )

    async def get_equipment_models(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[references.EquipmentModel]:

        """

        :param search_string: Search string (Искомая подстрока в названии или коде модели оборудования)
        :param page_size: Page size (Число возвращаемых записей. Не может превышать 100.)
        :param page_from_id: Page from id (ID модели оборудования, с которого начинается выборка записей. По умолчанию (если не задан параметр direction) выборка осуществляется в направлении от значения from_id в сторону уменьшения id модели.)
        :param page_direction: Page direction (Направление выборки. Доступно два значения: reverse, forward. reverse - возвращает записи, ID которых меньше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наибольшего значения id модели. forward - возвращает записи, ID которых больше значения from_id, если параметр from_id передан. При отсутствии параметра from_id выборка осуществляется от наименьшего значения id модели.)
        :return: Array of equipment models (Массив моделей оборудования)
        """
        return await self(
            references.GetEquipmentModelsRequest(
                search_string=search_string,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    async def create_equipment_model(
        self,
        name: str,
        code: str,
        equipment_kind_id: int,
        equipment_manufacturer_id: int,
        description: typing.Optional[str] = None,
    ) -> references.EquipmentModel:
        """

        :param name: Name (Название модели оборудования)
        :param code: Code (Код модели оборудования)
        :param equipment_kind_id: Equipment kind id (ID типа оборудования)
        :param equipment_manufacturer_id: Equipment manufacturer id (ID производителя оборудования)
        :param description: Description (Описание модели оборудования)
        :return: Equipment model (Модель оборудования)
        """
        return await self(
            references.CreateEquipmentModelRequest(
                name=name,
                code=code,
                equipment_kind_id=equipment_kind_id,
                equipment_manufacturer_id=equipment_manufacturer_id,
                description=description,
            )
        )

    async def update_equipment_model(
        self,
        equipment_model_id: int,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        visible: typing.Optional[bool] = None,
        equipment_kind_id: typing.Optional[int] = None,
        equipment_manufacturer_id: typing.Optional[int] = None,
    ) -> references.EquipmentModel:
        """
        Update equipment model (Обновление модели оборудования)

        :param equipment_model_id: Equipment model id (ID модели оборудования)
        :param name: Name (Название модели оборудования)
        :param description: Description (Описание модели оборудования)
        :param visible: Visible (Видимость модели оборудования)
        :param equipment_kind_id: Equipment kind id (ID типа оборудования)
        :param equipment_manufacturer_id: Equipment manufacturer id (ID производителя оборудования)
        :return: Equipment model (Модель оборудования)
        """

        return await self(
            references.UpdateEquipmentModelRequest(
                equipment_model_id=equipment_model_id,
                name=name,
                description=description,
                visible=visible,
                equipment_kind_id=equipment_kind_id,
                equipment_manufacturer_id=equipment_manufacturer_id,
            )
        )

    async def get_equipment_kinds(
        self,
        search_string: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        page_from_id: typing.Optional[int] = None,
        page_direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[references.EquipmentKind]:
        """

        :param search_string: Search string (Строка поиска)
        :param page_size: Page size (Количество элементов на странице)
        :param page_from_id: Page from id (ID элемента, с которого начинать выборку)
        :param page_direction: Page direction (Направление выборки ("reverse", "forward"))
        :return: Array of equipment kinds (Массив типов оборудования)
        """
        return await self(
            references.GetEquipmentKindsRequest(
                search_string=search_string,
                page_size=page_size,
                page_from_id=page_from_id,
                page_direction=page_direction,
            )
        )

    async def create_equipment_kind(
        self,
        name: str,
        code: str,
        description: typing.Optional[str] = None,
        parameter_codes: typing.Optional[typing.List[str]] = None,
    ) -> references.EquipmentKind:
        """

        :param name: Name (Название типа оборудования)
        :param code: Code (Код типа оборудования)
        :param description: Description (Описание типа оборудования)
        :param parameter_codes: Parameter codes (Массив из кодов связанных допополнительных атрибутов оборудования)
        :return: Equipment kind (Тип оборудования)
        """
        return await self(
            references.CreateEquipmentKindRequest(
                name=name,
                code=code,
                description=description,
                parameter_codes=parameter_codes,
            )
        )

    # price_lists
    async def get_price_lists(
        self,
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[price_lists.PriceList]:
        """

        :param size: Page size (Количество элементов на странице)
        :param from_id: Page from id (ID элемента, с которого начинать выборку)
        :param direction: Page direction (Направление выборки ("reverse", "forward"))
        :return: Array of price lists (Массив прайс-листов)
        """

        return await self(
            price_lists.GetPriceListListRequest(
                size=size, from_id=from_id, direction=direction
            )
        )

    async def get_price_list_services(
        self,
        price_list_id: int,
        types_: typing.List[typing.Literal["service", "work", "product"]],
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[price_lists.Service]:
        """

        :param price_list_id: Price list id (ID прайс-листа)
        :param types_: Types (Типы услуг)
        :param size: Page size (Количество элементов на странице)
        :param from_id: Page from id (ID элемента, с которого начинать выборку)
        :param direction: Page direction (Направление выборки ("reverse", "forward"))
        :return: Array of services (Массив услуг)
        """

        return await self(
            price_lists.GetPriceListServicesRequest(
                price_list_id=price_list_id,
                types_=types_,
                size=size,
                from_id=from_id,
                direction=direction,
            )
        )

    async def add_service_to_price_list(
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
    ) -> price_lists.Service:
        """

        :param price_list_id: Price list id (ID прайс-листа)
        :param code: Code (Код услуги/работы/товара)
        :param name: Name (Название услуги/работы/товара)
        :param type_: Type (Тип услуги/работы/товара)
        :param unit: Unit (Единица измерения)
        :param price: Price (Цена)
        :param nds: Nds (НДС)
        :param visible: Visible (Видимость)
        :param description: Description (Описание)
        :return: Service (Услуга/работа/товар)
        """

        return await self(
            price_lists.AddServiceToPriceListRequest(
                price_list_id=price_list_id,
                code=code,
                name=name,
                type_=type_,
                unit=unit,
                price=price,
                nds=nds,
                visible=visible,
                description=description,
            )
        )

    async def update_service_in_pricelist(
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
    ) -> price_lists.Service:
        """

        :param price_list_id: Price list id (ID прайс-листа)
        :param code: Code (Код услуги/работы/товара)
        :param name: Name (Название услуги/работы/товара)
        :param type_: Type (Тип услуги/работы/товара)
        :param unit: Unit (Единица измерения)
        :param price: Price (Цена)
        :param nds: Nds (НДС)
        :param visible: Visible (Видимость)
        :param description: Description (Описание)
        :return: Service (Услуга/работа/товар)
        """

        return await self(
            price_lists.UpdateServiceInPriceListRequest(
                price_list_id=price_list_id,
                code=code,
                name=name,
                type_=type_,
                unit=unit,
                price=price,
                nds=nds,
                visible=visible,
                description=description,
            )
        )

    async def get_available_services_for_issue(
        self,
        issue_id: int,
        search_string: str = None,
        size: typing.Optional[int] = None,
        from_id: typing.Optional[int] = None,
        direction: typing.Optional[typing.Literal["reverse", "forward"]] = None,
    ) -> typing.List[price_lists.ServiceWithPriceList]:
        """

        :param issue_id: Issue id (ID заявки)
        :param search_string: Search string (Строка поиска)
        :param size: Page size (Количество элементов на странице)
        :param from_id: Page from id (ID элемента, с которого начинать выборку)
        :param direction: Page direction (Направление выборки ("reverse", "forward"))
        :return: Array of services (Массив услуг)
        """

        return await self(
            price_lists.GetAvailableServicesForIssueRequest(
                issue_id=issue_id,
                search_string=search_string,
                size=size,
                from_id=from_id,
                direction=direction,
            )
        )
