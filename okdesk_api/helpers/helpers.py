import datetime
import typing
import enum


class AttributeFilterType(enum.Enum):
    DATE = "ftdate"
    DATETIME = "ftdatetime"
    CHECKBOX = "ftcheckbox"
    SELECT = "ftselect"
    MULTISELECT = "ftmultiselect"
    STRING = "ftstring"


class AttributeFilter:
    def __init__(self, code: str, field_type: AttributeFilterType, value: typing.Any):
        self.code = code
        self.field_type = field_type
        self.value = value

    def to_param(self, param_name) -> typing.Dict[str, str]:
        raise NotImplementedError


class AttributeFilterDate(AttributeFilter):
    def __init__(self, code: str, since: datetime.date, until: datetime.date):
        super().__init__(
            code, AttributeFilterType.DATE, {"since": since, "until": until}
        )

    def to_param(self, param_name) -> typing.Dict[str, str]:
        return {
            f"{param_name}[{self.code}_since]": self.value["since"].strftime(
                "%Y-%m-%d"
            ),
            f"{param_name}[{self.code}_until]": self.value["until"].strftime(
                "%Y-%m-%d"
            ),
        }


class AttributeFilterDatetime(AttributeFilter):
    def __init__(self, code: str, since: datetime.datetime, until: datetime.datetime):
        super().__init__(
            code, AttributeFilterType.DATETIME, {"since": since, "until": until}
        )

    def to_param(self, param_name) -> typing.Dict[str, str]:
        return {
            f"{param_name}[{self.code}_since]": self.value["since"].strftime(
                "%Y-%m-%d %H:%M"
            ),
            f"{param_name}[{self.code}_until]": self.value["until"].strftime(
                "%Y-%m-%d %H:%M"
            ),
        }


class AttributeFilterCheckbox(AttributeFilter):
    def __init__(self, code: str, value: bool):
        super().__init__(code, AttributeFilterType.CHECKBOX, value)

    def to_param(self, param_name) -> typing.Dict[str, str]:
        return {f"{param_name}[{self.code}]": str(self.value).lower()}


class AttributeFilterSelect(AttributeFilter):
    def __init__(self, code: str, value: typing.List[str]):
        super().__init__(code, AttributeFilterType.SELECT, value)

    def to_param(self, param_name) -> dict:
        to_return = {f"{param_name}[{self.code}][]": []}
        for value in self.value:
            to_return[f"{param_name}[{self.code}][]"].append(convert_param(value))
        return to_return


class AttributeFilterMultiselect(AttributeFilter):
    def __init__(self, code: str, value: typing.List[str]):
        super().__init__(code, AttributeFilterType.MULTISELECT, value)

    def to_param(self, param_name) -> dict:
        to_return = {f"{param_name}[{self.code}][]": []}
        for value in self.value:
            to_return[f"{param_name}[{self.code}][]"].append(convert_param(value))
        return to_return


class AttributeFilterString(AttributeFilter):
    def __init__(self, code: str, value: str):
        super().__init__(code, AttributeFilterType.STRING, value)

    def to_param(self, param_name) -> typing.Dict[str, str]:
        return {f"{param_name}[{self.code}]": self.value}


def convert_additional_attributes_filter(
    param_name, attributes: typing.List[AttributeFilter]
) -> dict:
    """
    Тип атрибута 	Тип значения 	Описание
    Дата 	string 	Доступны два типа значения: Код дополнительного атрибута_since - задает левую границу диапазона (С) и Код дополнительного атрибута_until - задает правую границу диапазона (По). Может быть передан один из параметров или оба параметра.
    Пример:
    custom_parameters[date_code_since]=2018-01-01
    custom_parameters[date_code_until]=2018-12-12

    Дата/время 	string 	Доступны два типа значения: Код дополнительного атрибута_since - задает левую границу диапазона (С) и Код дополнительного атрибута_until - задает правую границу диапазона (По). Может быть передан один из параметров или оба параметра.
    Пример:
    custom_parameters[datetime_code_since]=2018-01-01 01:01
    custom_parameters[datetime_code_until]=2018-12-12 12:12

    Чекбокс 	string 	Доступны два значения true и false.
    Пример:
    custom_parameters[checkbox_code]=true

    Значение из списка 	array of string 	Массив из значений списка.
    Пример:
    custom_parameters[list_code][]=list_value

    Набор значений из списка 	array of string 	Массив из значений списка.
    Пример:
    custom_parameters[list_code][]=list_value

    Строка 	string 	Значение строкового типа.
    Пример:
    custom_parameters[string_code]=string_value
    """
    new_dict = {}

    for attribute in attributes:
        if not isinstance(attribute, AttributeFilter):
            raise TypeError("AttributeFilter expected")

        new_dict.update(attribute.to_param(param_name))
    return new_dict


def convert_param(param) -> str:
    # converts python types to str URL params
    if isinstance(param, list):
        raise TypeError("List is not supported")
    elif isinstance(param, datetime.datetime):
        return param.isoformat()
    elif isinstance(param, datetime.date):
        return param.strftime("%Y-%m-%d")
    elif isinstance(param, dict):
        to_return = ""
        for key, value in param.items():
            to_return += f"{key}:{convert_param(value)},"
    elif isinstance(param, bool):
        return "true" if param else "false"
    elif isinstance(param, int):
        return str(param)
    elif isinstance(param, str):
        return param
    else:
        return str(param)
