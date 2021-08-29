import json
from typing import (
    Optional,
    Type,
)

import pydantic

from .openapi_models import (
    OpenAPISchema,
)


class ParserParam(pydantic.BaseModel):
    pass


class ParserResponse(pydantic.BaseModel):
    pass


class ParserHeader(pydantic.BaseModel):
    pass


class ParserOperation(pydantic.BaseModel):
    # For docs
    tags: list[str] = []
    summary: Optional[str]
    description: Optional[str]
    operation_id: Optional[str]
    parameters: list[ParserParam] = []
    request_body_model: Optional[Type[pydantic.BaseModel]]
    responses: list[ParserResponse] = []
    deprecated: bool = False
    # TODO: Support for many servers and security requirements
    # security: list[SecurityRequirement] = []
    # servers: list[Server] = []


class ParseResult(pydantic.BaseModel):
    # For docs
    api_title: str
    api_version: str
    base_url: Optional[str]
    common_headers: list[ParserHeader] = []
    common_params: list[ParserParam] = []
    operations: list[ParserOperation] = []


class OpenAPISchemaParser:
    def __init__(self, schema_json: str):
        self.schema = OpenAPISchema.parse_obj(json.loads(schema_json))
        self.__result: Optional[ParseResult] = None

    def parse(self) -> ParseResult:
        if self.__result is not None:
            return self.__result

        common_params = []
        common_headers = []
        operations = []

        self.__result = ParseResult(
            api_title=self.schema.info.title,
            api_version=self.schema.info.version,
            base_url=None,
            common_params=common_params,
            common_headers=common_headers,
            operations=operations
        )

        return self.__result
