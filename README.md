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
```python3
import string
from random import randint, choices
from dataclasses import dataclass
from uuid import uuid4

import uvicorn as uvicorn
from lagom import injectable, Container, Singleton
from marshmallow_jsonapi import fields
from starlette.applications import Starlette
from starlette_jsonapi.schema import JSONAPISchema

from resource import ResourceWithDI as BaseResource


@dataclass
class Engine:
    model: str
    horsepower: int
    id: int = uuid4().int


@dataclass
class Car:
    model: str
    engine: Engine
    id: int = uuid4().int


class RandomizedCarFactory:
    def __call__(self):
        def create_car():
            engine = Engine(model=self.random_model(), horsepower=randint(30, 300))
            car = Car(model=self.random_model(), engine=engine)
            return car
        return [create_car() for _ in range(5)]

    @classmethod
    def random_model(cls):
        return ''.join(choices(string.ascii_letters + string.digits, k=5))


class EngineSchema(JSONAPISchema):
    id = fields.Str(dump_only=True)
    model = fields.Str(required=True)
    horsepower = fields.Str(required=True)

    class Meta:
        type_ = 'engines'


class CarSchema(JSONAPISchema):
    id = fields.Str(dump_only=True)
    model = fields.Str(required=True)
    engine = fields.Nested(EngineSchema)

    class Meta:
        type_ = 'cars'
        self_route_many = 'cars:get_many'


class CarsResource(BaseResource):
    type_ = 'cars'
    schema = CarSchema

    async def get_many(self, interactor: RandomizedCarFactory = injectable, *args, **kwargs):
        data = interactor()
        payload = await self.serialize(data=data, many=True)
        return await self.to_response(payload)


if __name__ == '__main__':
    app = Starlette()

    """
    CarsResource will create an empty container which is possible in this
    example because RandomizedCarFactory lacks dependencies of its own,
    is not subclassed and can be constructed with no wiring whatsoever.
    """

    CarsResource.register_routes(app)

    """
    Passing dependencies.
    You can of course use an abstract type to switch implementations,
    change the type annotation in handler arguments accordingly.
    """

    # dependencies = Container()
    # dependencies[RandomizedCarFactory] = Singleton(RandomizedCarFactory)
    # CarsResource.register_routes(app, container=dependencies)

    uvicorn.run(app, host='localhost', port=8000)

    """
    Cars are available at http://localhost:8000/cars/
    """
```
