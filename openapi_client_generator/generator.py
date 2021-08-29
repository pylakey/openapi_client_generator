import httpx

from .parser import OpenAPISchemaParser


def generate(uri: str):
    parser = OpenAPISchemaParser(httpx.get(uri).text)
    result = parser.parse()

    # TODO: Use jinja template to create models.py file based on parser.schema with all models from OpenAPI schema
    # TODO: Use jinjs template to create client.py file based on parsing result
