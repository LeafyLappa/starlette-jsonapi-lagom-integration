"""
For use with starlette_jsonapi (https://github.com/vladmunteanu/starlette-jsonapi)
"""
from starlette_jsonapi.resource import BaseResource, BaseRelationshipResource
from lagom import Container


class ResourceWithDI(BaseResource):
    _dependency_container: Container

    @classmethod
    async def execute_handler(cls, request, request_context, handler_name, *args, **kwargs):
        resource = cls(request, request_context, *args, **kwargs)
        handler = getattr(resource, handler_name, None)
        handler_with_deps = cls._dependency_container.partial(handler)
        response = await handler_with_deps(*args, **kwargs)
        return response

    @classmethod
    def register_routes(cls, app, base_path: str = '', container: Container = Container()):
        cls._dependency_container = container
        super().register_routes(app, base_path)


class RelationshipResourceWithDI(BaseRelationshipResource):
    _dependency_container: Container

    @classmethod
    async def execute_handler(cls, request, request_context, handler_name, *args, **kwargs):
        resource = cls(request, request_context, *args, **kwargs)
        handler = getattr(resource, handler_name, None)
        handler_with_deps = cls._dependency_container.partial(handler)
        response = await handler_with_deps(*args, **kwargs)
        return response

    @classmethod
    def register_routes(cls, container: Container = Container(), *args, **kwargs):
        cls._dependency_container = container
        super().register_routes(*args, **kwargs)
