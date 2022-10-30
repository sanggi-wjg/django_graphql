from importlib import import_module

import yaml
from django.conf import settings
from django.core.management import BaseCommand

from app.core.colorful import yellow, green


class Scheme:

    def __init__(self, name, klass, input):
        self.name = name
        self.klass = klass
        self.input = input


def get_schemas():
    return set([
        (name, klass)
        for name, klass in import_module(settings.SCHEMA_CONF).__dict__.items()
        if 'Query' in name or 'Mutation' in name
    ])


def get_klass_description(klass, default=None):
    desc = default
    if hasattr(klass, '_meta') and hasattr(klass._meta, 'description'):
        if klass._meta.description is not None:
            desc = klass._meta.description

    return desc


def get_klass_request_body(klass):
    request_body = {}
    if hasattr(klass, "_meta") and hasattr(klass._meta, 'arguments'):
        input = klass._meta.arguments.get('input')
        if input is None:
            return request_body

        request_body = {
            'required': input.kwargs.get('required', False),
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            field: {
                                'type': field_klass.type.of_type._meta.name.lower()
                            }
                            for field, field_klass in input._meta.fields.items()
                        }
                    }
                }
            }
        }
    return request_body


def get_klass_responses(klass):
    responses = {
        200: {'description': "whether success or fail, it always 200"}
    }
    if hasattr(klass, 'help'):
        exceptions = [msg.strip() for msg in getattr(klass, 'help').strip().split('\n')]

        for exception in exceptions:
            exc, exc_msg = exception.split(":")
            responses[exc.strip()] = {
                'description': exc_msg.strip()
            }
    return responses


def create_yaml(schemas):
    content = dict()

    content['openapi'] = "3.0.0"

    content['info'] = {
        'title': "OpenAPI Demo",
        'version': "0.0.1",
    }

    content['externalDocs'] = {
        'description': 'OpenAPI Demo',
        'url': 'http://localhost/graphql'
    }

    content['servers'] = [
        {
            'url': 'http://localhost:{port}/graphql',
            'variables': {
                'port': {
                    'enum': ['8000'],
                    'default': '8000'
                },
            }
        },
    ]

    content['tags'] = [
        {'name': 'Query', 'description': "쿼리"},
        {'name': 'Mutation', 'description': "뮤테이션"}
    ]

    content['paths'] = dict()
    for name, klass in schemas:
        content['paths'][f"/{name}"] = {
            'summary': name,
            'post': {
                'tags': ["Query" if "Query" in name else "Mutation"],
                'summary': get_klass_description(klass, default=name),
                'requestBody': get_klass_request_body(klass),
                'responses': get_klass_responses(klass)
            }
        }

    return yaml.safe_dump(content, allow_unicode=True, sort_keys=False)


class SchemaGenerator:

    def __init__(self):
        self.schemas = get_schemas()

    def generate(self):
        yaml_content = create_yaml(self.schemas)
        yellow(yaml_content)

        # with open(settings.STATICFILES_DIRS[0], 'w') as f:
        #     f.write(yaml_content)


class Command(BaseCommand):
    help = 'Create schema docs'

    def handle(self, *args, **options):
        # https://editor.swagger.io/
        # https://swagger.io/docs/specification/basic-structure/
        # https://support.smartbear.com/swaggerhub/docs/collaboration/index.html
        schema_generator = SchemaGenerator()
        schema_generator.generate()
