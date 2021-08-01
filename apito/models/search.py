from typing import Literal, Union

from pydantic import BaseModel, Field


class ItemCoordinates(BaseModel):
    lat: float
    lng: float


class ItemCategory(BaseModel):
    id: int
    name: str


class ItemValue(BaseModel):
    id: int
    category: ItemCategory
    time: int
    title: str
    images: dict
    price: str
    location: str
    address: str
    coords: ItemCoordinates
    uri: str = Field(...,  alias="uri_mweb")
    description: str = Field('')


class SearchItemValueItemFigni(BaseModel):
    type: str
    value: ItemValue


class SearchItemValueFigni(BaseModel):
    list: list[SearchItemValueItemFigni]


class SearchItemFigni(BaseModel):
    type: str
    value: SearchItemValueFigni


class SearchItem(BaseModel):
    type: Literal['item', 'xlItem']
    value: ItemValue


class GroupTitleItemValue(BaseModel):
    title: str


class GroupTitleItem(BaseModel):
    type: str
    value: GroupTitleItemValue


class SearchResult(BaseModel):
    display_type: str = Field(..., alias='displayType')
    count: int
    total_count: int = Field(..., alias='totalCount')
    main_count: int = Field(..., alias='mainCount')
    last_stamp: int = Field(..., alias='lastStamp')
    items: list[Union[SearchItem, SearchItemFigni, GroupTitleItem]]


class SearchError(BaseModel):
    message: dict


class SearchAnswer(BaseModel):
    status: Literal['ok', 'incorrect-data', 'bad-request']
    result: Union[SearchResult, SearchError]
