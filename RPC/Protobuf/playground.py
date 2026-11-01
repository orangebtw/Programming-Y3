from datetime import datetime, timezone

from library.v1 import library_pb2

book = library_pb2.Book(id=1, title="Solaris", genre=library_pb2.GENRE_FICTION)
book.authors.add(name="Stanisław Lem", birth_year=1921)
book.attributes["language"] = "pl"
book.attributes["publisher"] = "MON"
book.published_at.FromDatetime(datetime(1961, 1, 1, tzinfo=timezone.utc))
book.isbn = "978-0-15-602760-1"

print(book)   # текстовое представление для отладки

print("-------------------------------------------------------------------------------------------------------------")
data = book.SerializeToString()
print(type(data).__name__, len(data), "байт")
print(data.hex(" "))

restored = library_pb2.Book.FromString(data)
print("Объекты равны:", restored == book)
print("Заголовок после разбора:", restored)

print("-------------------------------------------------------------------------------------------------------------")
from google.protobuf import json_format

as_json = json_format.MessageToJson(book, indent=None)
print(as_json)
print()
print("JSON:    ", len(as_json.encode()), "байт")
print("protobuf:", len(data), "байт")

# Имена полей как в .proto
print(json_format.MessageToDict(book, preserving_proto_field_name=True)["published_at"])

print("-------------------------------------------------------------------------------------------------------------")
empty = library_pb2.Book()
print(repr(empty.title), empty.id, empty.genre, list(empty.authors), dict(empty.attributes))
print("Пустое сообщение занимает", len(empty.SerializeToString()), "байт")

# Поле-сообщение отслеживает наличие всегда
print("published_at задано?", empty.HasField("published_at"))

# optional-скаляр тоже отслеживает наличие
author = library_pb2.Author(name="Lem")
print("birth_year задано?", author.HasField("birth_year"))
author.birth_year = 0
print("birth_year задано после присваивания 0?", author.HasField("birth_year"))

# Обычный скаляр наличие не отслеживает
try:
    empty.HasField("title")
except ValueError as error:
    print("ValueError:", error)

print("-------------------------------------------------------------------------------------------------------------")
WIRE_TYPES = {0: "VARINT", 1: "I64", 2: "LEN", 5: "I32"}


def read_varint(data: bytes, pos: int) -> tuple[int, int]:
    """Читает varint начиная с позиции pos. Возвращает (значение, новая позиция)."""
    result = shift = 0
    while True:
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift     # младшие 7 бит — полезные данные
        if not byte & 0x80:                   # старший бит 0 — последний байт числа
            return result, pos
        shift += 7


def dump_fields(data: bytes, indent: str = "") -> None:
    """Печатает поля сообщения без знания схемы."""
    pos = 0
    while pos < len(data):
        key, pos = read_varint(data, pos)
        field_number, wire_type = key >> 3, key & 0b111
        if wire_type == 0:
            value, pos = read_varint(data, pos)
        elif wire_type == 1:
            value, pos = data[pos:pos + 8], pos + 8
        elif wire_type == 2:
            length, pos = read_varint(data, pos)
            value, pos = data[pos:pos + length], pos + length
        elif wire_type == 5:
            value, pos = data[pos:pos + 4], pos + 4
        else:
            raise ValueError(f"Неподдерживаемый wire type {wire_type}")
        print(f"{indent}поле {field_number:>2}  {WIRE_TYPES[wire_type]:<6}  {value!r}")


dump_fields(book.SerializeToString())
dump_fields(book.authors[0].SerializeToString(), indent="  ")