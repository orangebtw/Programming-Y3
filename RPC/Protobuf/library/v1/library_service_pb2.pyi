from library.v1 import library_pb2 as _library_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetBookRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ListBooksRequest(_message.Message):
    __slots__ = ("genre",)
    GENRE_FIELD_NUMBER: _ClassVar[int]
    genre: _library_pb2.Genre
    def __init__(self, genre: _Optional[_Union[_library_pb2.Genre, str]] = ...) -> None: ...

class BuildReportRequest(_message.Message):
    __slots__ = ("work_seconds",)
    WORK_SECONDS_FIELD_NUMBER: _ClassVar[int]
    work_seconds: float
    def __init__(self, work_seconds: _Optional[float] = ...) -> None: ...

class Report(_message.Message):
    __slots__ = ("total_books", "books_by_genre")
    class BooksByGenreEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTAL_BOOKS_FIELD_NUMBER: _ClassVar[int]
    BOOKS_BY_GENRE_FIELD_NUMBER: _ClassVar[int]
    total_books: int
    books_by_genre: _containers.ScalarMap[str, int]
    def __init__(self, total_books: _Optional[int] = ..., books_by_genre: _Optional[_Mapping[str, int]] = ...) -> None: ...
