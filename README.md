# starlette-jsonapi-lagom-integration
Dependency Injection for [starlette_jsonapi](https://github.com/vladmunteanu/starlette-jsonapi)

## Usage
Resource class has to inherit from `ResourceWithDI` (alternatively `RelationshipResourceWithDI` if it's a relationship resource).

Add injections to the handler methods as arguments using the `injectable` marker:
```python3
async def get(self, id, interactor: FooInteractor = injectable, *args, **kwargs):
    ...

async def get_many(self, interactor: BarInteractor = injectable, *args, **kwargs):
    ...

```
Pass your container when registering routes for the resource:
```python3
resource.register_routes(self.starlette, self.root, self.dependency_container)
```
Note that you don't have to do this, in which case a new (empty) container will be used.

## Complete example
(todo)
