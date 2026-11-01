import time

import grpc

import library_server
from library.v1 import library_pb2, library_service_pb2, library_service_pb2_grpc

library_grpc_server = library_server.serve(port=50052)
library_channel = grpc.insecure_channel("localhost:50052")
library_stub = library_service_pb2_grpc.LibraryServiceStub(library_channel)
print("Сервер LibraryService запущен")

book, call = library_stub.GetBook.with_call(
    library_service_pb2.GetBookRequest(id=1),
    metadata=[("x-request-id", "req-42")],
    timeout=2,
)
print(book.title, "—", book.authors[0].name)
print("Метаданные ответа:", dict(call.trailing_metadata()))

for book_id in (2, 999, 0):
    try:
        found = library_stub.GetBook(library_service_pb2.GetBookRequest(id=book_id), timeout=2)
        print(f"id={book_id}: {found.title}")
    except grpc.RpcError as error:
        print(f"id={book_id}: {error.code().name} — {error.details()}")

# Серверный поток с фильтром
for found in library_stub.ListBooks(library_service_pb2.ListBooksRequest(genre=library_pb2.GENRE_FICTION), timeout=5):
    print(found.id, found.title)

auth = [("authorization", f"Bearer {library_server.API_TOKEN}")]
scenarios = [
    ("без токена", [], 1.0, 5),
    ("короткий дедлайн", auth, 2.0, 0.5),
    ("успех", auth, 1.0, 5),
]
for title, metadata, work_seconds, timeout in scenarios:
    started = time.monotonic()
    try:
        report = library_stub.BuildReport(
            library_service_pb2.BuildReportRequest(work_seconds=work_seconds),
            metadata=metadata,
            timeout=timeout,
        )
        result = f"OK: {report.total_books} книги, {dict(report.books_by_genre)}"
    except grpc.RpcError as error:
        result = f"{error.code().name} — {error.details()}"
    print(f"{title:<18} {time.monotonic() - started:4.1f} с  {result}")