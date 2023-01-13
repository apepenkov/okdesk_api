> OkDesk API
> ==========
---
## This is an _async_ python3.6+ wrapper for the OkDesk API. It is a work in progress.


# Structure
The OkDesk API is structured as follows:

* `okdesk_api/api/*` - contains raw API calls, and classes.
* `okdesk_api/helpers` - contains helper functions.
* `okdesk_api/errors` - contains error class
* `okdesk_api/types` - contains some common classes, such as 
  * ApiRequest (base for all API requests)
  * OkDeskBaseClass (base for all OkDesk classes)
  * typehinted dicts. (for example, `IdNamePair` is a dict with type hints for all keys: {id: int, name: str})
* `okdesk_api/client` - contains the main client class (wrapper for the API).

# Api calls
Each Api caller is an instance of
```python
class ApiRequest:
    # method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH"], url: str, **kwargs
    def to_request(self) -> dict:
        raise NotImplementedError

    def from_response(self, result):
        raise NotImplementedError
```
Example of an ApiRequest:
```python
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
```
When you want to call API, you have to either use wrapped method from `client`, or
call it via 
```python
await client(GetIssueRequest(issue_id=0))
```
It will:
1. Call `GetIssueRequest.to_request()`
2. Use returned dict to make a request (populating api_key, etc)
3. Call `GetIssueRequest.from_response()` with the result of the request as an argument, and return the result.

Alternatively, you can use: (preferred way, as it provides typehints)
```python
await client.get_issue(issue_id=0)
```

`ApiRequest`s may have such arguments, as:
* basic python types (int, str, list, bool, etc)
* `datetime.datetime` (will be converted according to specification)
* `datetime.date`  (will be converted according to specification)
* **type-hinted dicts** (aka `typing.TypedDict`) from `okdesk_api/types`
* classes. If class is required, it may be nested in ApiRequest, itself, or used from some api file.
* `okdesk_api.types.Attachment` (typed dict) - Local file to be uploaded to OkDesk. [go](#uploading-files)
* helpers/AttributeFilter [go](#attribute-filter)
# Uploading files
To upload a file, you have to use `okdesk_api.types.Attachment` class.
```python
request = AddMaintenanceEntityAttachmentRequest(
    maintenance_entity_id=123,
    attachments=[
      {
        "attachment": "path/to/file",
        "description": "Some description", # optional
        "is_public": True, # optional, not every endpoint supports this
      }
    ]
)
result = await client(request)
```
Attachment will be uploaded as multipart/form-data, mime type will be guessed from file extension, filename will be used from path. 

# Attribute Filter

`AttributeFilter` - base for the following filters:
* `AttributeFilterDate` - filter by date
* `AttributeFilterDateTime` - filter by datetime
* `AttributeFilterCheckbox` - filter by checkbox on/off
* `AttributeFilterSelect` - filter by select (one of the options)
* `AttributeFilterMultiselect` - filter by multiselect (one or more options)
* `AttributeFilterString` - filter by string 

Those filters are used in such requests, as `companies.GetCompanyListRequest`, `issues.GetIssuesListIdRequest`, etc.

They are passed as an array.

Make sure you checked that the API endpoint you are using is supported by the filter you are using, because some filters are not supported by some endpoints.

# Type hints

**All requests are type-hinted**, so you can use IDE's autocomplete to find out what arguments are required.

Also each request class includes a link to the documentation, and a description of the arguments.

Responses are only type-hinted, if you use wrapped methods from `client`, or if you use `from_response` method.

I would highly recommend looking at type hints, as they are very informative.


