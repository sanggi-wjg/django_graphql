from importlib import import_module

import yaml
from django.conf import settings
from django.core.management import BaseCommand

from app.core.colorful import yellow


class Scheme:

    def __init__(self, name, klass, input):
        self.name = name
        self.klass = klass
        self.input = input


def get_schemas():
    schemas = set()
    for name, klass in import_module(settings.SCHEMA_CONF).__dict__.items():
        if 'Query' in name or 'Mutation' in name:
            schemas.add((name, klass))

    return schemas


def get_klass_description(klass, default=None):
    desc = default
    if hasattr(klass, '_meta') and hasattr(klass._meta, 'description'):
        if klass._meta.description is not None:
            desc = klass._meta.description

    return desc


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
                'responses': {
                    200: {
                        'description': "200 success"
                    }
                }
            }
        }

    return yaml.safe_dump(content, allow_unicode=True, sort_keys=False)


class SchemaGenerator:

    def __init__(self):
        self.schemas = get_schemas()

    def generate(self):
        yaml_content = create_yaml(self.schemas)
        yellow(yaml_content)


class Command(BaseCommand):
    help = 'Create schema docs'

    def handle(self, *args, **options):
        # https://editor.swagger.io/
        # https://support.smartbear.com/swaggerhub/docs/collaboration/index.html
        schema_generator = SchemaGenerator()
        schema_generator.generate()
