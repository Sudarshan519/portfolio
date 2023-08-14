from datetime import date
from typing import Optional, TypeVar, Generic, List

from fastapi import HTTPException
from pydantic import  BaseModel, validator,create_model 
from pydantic.generics import GenericModel
from pyparsing import Any 
T = TypeVar('T')

class ResponseSchema(GenericModel, Generic[T]):#(BaseModel):#
    status: str
    data: Optional[T] = None


class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]


def create_data_model(
        model:type=[BaseModel],
        plural:bool=False,
        custom_plural_name: Optional[str] = None,
    **kwargs: Any,
)-> type[BaseModel]:
    data_field_name = model.__name__.lower()
    if plural:
        model_name = f"Multiple{model.__name__}"
        if custom_plural_name:
            data_field_name = custom_plural_name
        else:
            data_field_name += "s"
        kwargs[data_field_name] = (list[model], ...)  # type: ignore[valid-type]
    else:
        model_name = f"Single{model.__name__}"
        kwargs[data_field_name] = (model, ...)
    return create_model(model_name, **kwargs)
# SingleJobApplication=create_data_model(ShowJobApplication)
# BaseResponse=create_data_model(PageResponse[SingleJobApplication ])

class Foo(BaseModel):
    a: str
    b: int


class Bar(BaseModel):
    x: float



SingleFoo = create_data_model(Foo)
MultipleBar = create_data_model(Bar, plural=True)
M = TypeVar("M", bound=BaseModel)
class GenericResponse(GenericModel, Generic[M]):
    status: str="success"
    data: M