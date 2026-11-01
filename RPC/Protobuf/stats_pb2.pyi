from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CountdownRequest(_message.Message):
    __slots__ = ("start",)
    START_FIELD_NUMBER: _ClassVar[int]
    start: int
    def __init__(self, start: _Optional[int] = ...) -> None: ...

class CountdownReply(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class Number(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class SumReply(_message.Message):
    __slots__ = ("total", "count")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    total: float
    count: int
    def __init__(self, total: _Optional[float] = ..., count: _Optional[int] = ...) -> None: ...

class AverageReply(_message.Message):
    __slots__ = ("average", "count")
    AVERAGE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    average: float
    count: int
    def __init__(self, average: _Optional[float] = ..., count: _Optional[int] = ...) -> None: ...
