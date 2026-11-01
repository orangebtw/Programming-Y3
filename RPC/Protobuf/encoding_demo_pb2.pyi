from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Demo(_message.Message):
    __slots__ = ("a", "b", "negative", "zigzag", "nums")
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    ZIGZAG_FIELD_NUMBER: _ClassVar[int]
    NUMS_FIELD_NUMBER: _ClassVar[int]
    a: int
    b: str
    negative: int
    zigzag: int
    nums: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, a: _Optional[int] = ..., b: _Optional[str] = ..., negative: _Optional[int] = ..., zigzag: _Optional[int] = ..., nums: _Optional[_Iterable[int]] = ...) -> None: ...
