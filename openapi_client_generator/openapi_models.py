from __future__ import annotations

from enum import Enum
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
)

import pydantic
from pydantic import (
    EmailStr,
    HttpUrl,
)


class BaseModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True


class RootIterable(BaseModel):
    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class ParameterIn(str, Enum):
    query = 'query'
    header = 'header'
    path = 'path'
    cookie = 'cookie'


class SecuritySchemeType(str, Enum):
    api_key = 'apiKey'
    http = 'http'
    oauth2 = 'oauth2'
    open_id_connect = 'openIdConnect'


class SecuritySchemeIn(str, Enum):
    query = 'query'
    header = 'header'
    cookie = 'cookie'


MappingKey = TypeVar('MappingKey')
MappingValue = TypeVar('MappingValue')


class Mapping(RootIterable, Generic[MappingKey, MappingValue]):
    __root__: dict[MappingKey, MappingValue]


class StrMapping(Mapping[str, MappingValue], Generic[MappingValue]):
    pass


class License(BaseModel):
    name: str
    url: Optional[HttpUrl]


class Contact(BaseModel):
    name: Optional[str]
    url: Optional[HttpUrl]
    email: Optional[EmailStr]


class Info(BaseModel):
    title: str
    description: Optional[HttpUrl]
    terms_of_service: Optional[str]
    contact: Optional[Contact]
    license: Optional[License]
    version: str


class ExternalDocs(BaseModel):
    url: HttpUrl
    description: Optional[str]


class Reference(BaseModel):
    ref: Optional[str] = pydantic.Field(None, alias="$ref")

    class Config(pydantic.BaseConfig):
        allow_population_by_field_name = True
        extra = pydantic.Extra.allow


class Parameter(BaseModel):
    name: str
    _in: ParameterIn
    description: Optional[str]
    required: bool = False
    deprecated: Optional[bool] = False
    allow_empty_value: Optional[bool] = False


# https://swagger.io/specification/#runtime-expression
ConstantOrExpression = Union[Any, str]


class Link(BaseModel):
    operation_ref: Optional[str]
    operation_id: Optional[str]
    parameters: dict[str, ConstantOrExpression]
    request_body: Optional[ConstantOrExpression]
    description: Optional[str]
    server: Optional[Server]


class Header(Parameter):
    name: Any = None
    _in: Any = None


class Headers(StrMapping[Union[Header, Reference]]):
    pass


class Links(StrMapping[Union[Link, Reference]]):
    pass


class Response(BaseModel):
    description: str
    headers: Optional[Headers]
    content: Optional[Content]
    links: Optional[Links]


class Responses(StrMapping[Union[Response, Reference]]):
    pass


class Operation(BaseModel):
    tags: list[str] = []
    summary: Optional[str]
    description: Optional[str]
    external_docs: Optional[ExternalDocs]
    operation_id: Optional[str]
    parameters: list[Union[Parameter, Reference]] = []
    request_body: Optional[Union[RequestBody, Reference]]
    responses: Responses
    callbacks: Optional[Callbacks]
    deprecated: bool = False
    security: list[SecurityRequirement] = []
    servers: list[Server] = []


class Schema(BaseModel):
    # TODO: Fill properties
    pass


class PathItem(BaseModel):
    ref: Optional[str] = pydantic.Field(None, alias="$ref")
    summary: Optional[str]
    description: Optional[str]
    servers: list[Server] = []
    parameters: list[Union[Parameter, Reference]] = []
    get: Optional[Operation]
    put: Optional[Operation]
    post: Optional[Operation]
    delete: Optional[Operation]
    options: Optional[Operation]
    head: Optional[Operation]
    patch: Optional[Operation]
    trace: Optional[Operation]


class ServerVariable(BaseModel):
    enum: list[str] = []
    default: str
    description: Optional[str]


class Server(BaseModel):
    url: str
    description: Optional[str]
    variables: StrMapping[ServerVariable]


class Encoding(BaseModel):
    content_type: str
    headers: Headers
    style: str
    explode: bool = False
    allow_reversed: bool = False


class Example(BaseModel):
    summary: Optional[str]
    description: Optional[str]
    value: Optional[Any]
    external_value: Optional[str]


class MediaType(BaseModel):
    _schema: Optional[Union[Schema, Reference]] = pydantic.Field(None, alias='schema')
    example: Optional[Any]
    examples: Optional[Examples]
    encoding: Optional[Encodings]


class Callback(StrMapping[PathItem]):
    pass


class Content(StrMapping[MediaType]):
    pass


class Schemas(StrMapping[Union[Schema, Reference]]):
    pass


class Parameters(StrMapping[Union[Parameter, Reference]]):
    pass


class Callbacks(StrMapping[Union[Callback, Reference]]):
    pass


class SecurityRequirement(StrMapping[list[str]]):
    pass


class Paths(StrMapping[PathItem]):
    pass


class OAuthFlowScopes(StrMapping[str]):
    pass


class Examples(StrMapping[Union[Example, Reference]]):
    pass


class Encodings(StrMapping[Encoding]):
    pass


class RequestBody(BaseModel):
    description: Optional[str]
    content: Content
    required: bool = False


class OAuthFlow(BaseModel):
    authorization_url: HttpUrl
    token_url: HttpUrl
    refresh_url: Optional[HttpUrl]
    scopes: OAuthFlowScopes


class OAuthFlows(BaseModel):
    implicit: Optional[OAuthFlow]
    password: Optional[OAuthFlow]
    client_credentials: Optional[OAuthFlow]
    authorization_code: Optional[OAuthFlow]


class SecurityScheme(BaseModel):
    type: SecuritySchemeType
    description: Optional[str]
    name: str
    scheme: str
    _in: SecuritySchemeIn
    bearer_format: Optional[str]
    flows: OAuthFlows


class RequestBodies(StrMapping[Union[RequestBody, Reference]]):
    pass


class SecuritySchemes(StrMapping[Union[SecurityScheme, Reference]]):
    pass


class Components(BaseModel):
    schemas: Optional[Schemas]
    responses: Optional[Responses]
    parameters: Optional[Parameters]
    examples: Optional[Examples]
    request_bodies: Optional[RequestBodies]
    headers: Optional[Headers]
    security_schemes: Optional[SecuritySchemes]
    links: Optional[Links]
    callbacks: Optional[Callbacks]


class Tag(BaseModel):
    name: str
    description: Optional[str]
    external_docs: Optional[ExternalDocs]


class OpenAPISchema(BaseModel):
    openapi: str
    info: Info
    servers: Optional[list[Server]]
    paths: Paths = {}
    components: Optional[Components]
    security: list[SecurityRequirement] = [{}]
    tags: list[Tag] = []
    external_docs: Optional[ExternalDocs]
