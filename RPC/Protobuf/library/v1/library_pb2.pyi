import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Genre(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENRE_UNSPECIFIED: _ClassVar[Genre]
    GENRE_FICTION: _ClassVar[Genre]
    GENRE_SCIENCE: _ClassVar[Genre]
    GENRE_HISTORY: _ClassVar[Genre]
GENRE_UNSPECIFIED: Genre
GENRE_FICTION: Genre
GENRE_SCIENCE: Genre
GENRE_HISTORY: Genre

class Author(_message.Message):
    __slots__ = ("name", "birth_year")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BIRTH_YEAR_FIELD_NUMBER: _ClassVar[int]
    name: str
    birth_year: int
    def __init__(self, name: _Optional[str] = ..., birth_year: _Optional[int] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("id", "title", "authors", "genre", "attributes", "published_at", "isbn", "ebook_url")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHORS_FIELD_NUMBER: _ClassVar[int]
    GENRE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_AT_FIELD_NUMBER: _ClassVar[int]
    ISBN_FIELD_NUMBER: _ClassVar[int]
    EBOOK_URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    authors: _containers.RepeatedCompositeFieldContainer[Author]
    genre: Genre
    attributes: _containers.ScalarMap[str, str]
    published_at: _timestamp_pb2.Timestamp
    isbn: str
    ebook_url: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., authors: _Optional[_Iterable[_Union[Author, _Mapping]]] = ..., genre: _Optional[_Union[Genre, str]] = ..., attributes: _Optional[_Mapping[str, str]] = ..., published_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., isbn: _Optional[str] = ..., ebook_url: _Optional[str] = ...) -> None: ...

class Catalog(_message.Message):
    __slots__ = ("books",)
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...
