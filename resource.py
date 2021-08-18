from starlette_jsonapi.resource import BaseResource, BaseRelationshipResource
from lagom import Container


class ResourceWithDI(BaseResource):
    # TODO: docstring
    dependency_container: Container

    @classmethod
    async def execute_handler(cls, request, request_context, handler_name, *args, **kwargs):
        resource = cls(request, request_context, *args, **kwargs)
        handler = getattr(resource, handler_name, None)
        handler_with_deps = cls.dependency_container.partial(handler)
        response = await handler_with_deps(*args, **kwargs)
        return response

    @classmethod
    def register_routes(cls, app, base_path: str = '', container: Container = Container()):
        cls.dependency_container = container
        super().register_routes(app, base_path)


# TODO: override execute_handler()
class RelationshipResourceWithDI(BaseRelationshipResource):
    # TODO: docstring
    dependency_container: Container

    @classmethod
    def register_routes(cls, container: Container = Container(), *args, **kwargs):
        cls.dependency_container = container
        super().register_routes(*args, **kwargs)
