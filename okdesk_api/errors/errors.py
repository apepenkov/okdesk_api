import typing


def dict_errors_to_errors(in_errors: dict) -> list:
    """
    example: {
    "created_until": [
      "Неверный формат даты"
    ],
    "observer_ids": {
      "1": [
        "должно иметь тип integer"
      ]
    },
    "page": {
      "size": [
        "должно быть меньше или равно 100"
      ],
      "direction": [
        "должен быть одним из: reverse, forward"
      ],
      "from_id": [
        "должно иметь тип integer"
      ]
    }
  }

    should be converted to:
    [
    "created_until: Неверный формат даты",
    "observer_ids.1: должно иметь тип integer",
    "page.size: должно быть меньше или равно 100",
    "page.direction: должен быть одним из: reverse, forward",
    "page.from_id: должно иметь тип integer"
    ]

    :param in_errors: an error dictionary
    :return: a list of errors
    """
    errors = []
    # Uses recursion instead of a stack, because it won't be too deep
    for key, value in in_errors.items():
        if isinstance(value, list):
            for error in value:
                errors.append(f"{key}: {error}")
        elif isinstance(value, dict):
            for error in dict_errors_to_errors(value):
                errors.append(f"{key}.{error}")
        else:
            raise ValueError(f"Unknown value type: {type(value)}")

    return errors


class OkDeskError(Exception):
    def __init__(
        self,
        json_error: typing.Union[dict, list],
    ):
        self.messages = []
        if isinstance(json_error, list):
            self.messages = str(json_error)
        elif isinstance(json_error, dict):
            self.messages = dict_errors_to_errors(json_error)
        else:
            self.messages.append("Can't parse error, raw: " + str(json_error))

    def __str__(self):
        return "\n".join(self.messages)
