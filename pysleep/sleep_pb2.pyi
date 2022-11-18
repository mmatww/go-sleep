from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SleepReply(_message.Message):
    __slots__ = ["id", "label", "sleep", "timestamp"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SLEEP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    sleep: int
    timestamp: str
    def __init__(self, id: _Optional[str] = ..., label: _Optional[str] = ..., sleep: _Optional[int] = ..., timestamp: _Optional[str] = ...) -> None: ...

class SleepRequest(_message.Message):
    __slots__ = ["id", "label", "sleep"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SLEEP_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    sleep: int
    def __init__(self, id: _Optional[str] = ..., label: _Optional[str] = ..., sleep: _Optional[int] = ...) -> None: ...
