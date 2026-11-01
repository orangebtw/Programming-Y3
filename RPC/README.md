# Программирование. Лабораторная работа «RPC. gRPC. Protobuf»

### Структура папок
* Microservices -- Приложение Marketplace на FastAPI
* Protobuf -- Знакомство с Protocol Buffers

## Protobuf

### Выполенные задания
1. Добавьте в Greeter метод SayGoodbye с собственными сообщениями запроса и ответа. Перегенерируйте код, реализуйте метод и вызовите его из клиента.

**✅ Выполнено в коммите 7d4aa093ff28762c78f5a37722d598a6f201f028.**
```diff
--- a/RPC/Protobuf/greeter_client.py
+++ b/RPC/Protobuf/greeter_client.py
 def run() -> None:
         print("Greeter client received:", response.message)
         response = stub.SayMyName(helloworld_pb2.MyNameRequest(name="Heisenberg"), timeout=5)
         print(response.message)
+        response = stub.SayGoodbye(helloworld_pb2.GoodbyeRequest(name="my friend"), timeout=5)
+        print(response.message)
 
 
 if __name__ == "__main__":
--- a/RPC/Protobuf/greeter_service.py
+++ b/RPC/Protobuf/greeter_service.py
 class Greeter(helloworld_pb2_grpc.GreeterServicer):
             message=f"ΓÇö You're {request.name}.\nΓÇö You're goddamn right."
         )
 
+    def SayGoodbye(self, request, context):
+        return helloworld_pb2.GoodbyeReply(message=f"Bye bye, {request.name} :(")
+
 
 def serve(port: int = 50051) -> None:
     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
--- a/RPC/Protobuf/protos/helloworld.proto
+++ b/RPC/Protobuf/protos/helloworld.proto
 service Greeter {
   rpc SayHello (HelloRequest) returns (HelloReply);
   rpc SayHelloAgain (HelloRequest) returns (HelloReply);
   rpc SayMyName (MyNameRequest) returns (MyNameReply);
+  rpc SayGoodbye (GoodbyeRequest) returns (GoodbyeReply);
 }
 
 message MyNameRequest {
 
 message MyNameReply {
   string message = 1;
+}
+
+message GoodbyeRequest {
+    string name = 1;
+}
+
+message GoodbyeReply {
+    string message = 1;
 }
\ No newline at end of file
```
2. Сколько байтов займёт сообщение Demo(a=300)? Проверьте ответ, вычислив его вручную по правилам varint.

**Решение:**
1) Поле `a` -- int32 (VARINT, код 0) с индексом 1, значит `(1 << 3) | 0 = 8` -- первый байт равен `0x08`.
2) Число 300 в двоичном формате -- `100101100`, берём младшие 7 бит, устанавливаем самый старший бит в значение 1, получается `10101100` или `0xAC` -- это второй байт.
3) Смещаем оригинальное число (`300`) на семь бит вправо, получается `000000010` или `0x02` -- это третий байт.

**Проверка:**
```python
import encoding_demo_pb2 as ed
raw = ed.Demo(a=300).SerializeToString()
print(f"{len(raw)} байт: {raw.hex(' ')}")
# 3 байт: 08 ac 02
```

## Microservices
Простое приложение использующее gRPC и Protocol Buffers.

Ключевые решения:
  * Канал gRPC создаётся один раз при старте приложения (lifespan) и закрывается при остановке. Создавать канал на каждый HTTP-запрос дорого.
  * Используется асинхронный клиент grpc.aio, потому что обработчики FastAPI асинхронные: ожидание ответа Recommendations не блокирует обработку других запросов.
  * Адрес сервиса берётся из переменной окружения RECOMMENDATIONS_HOST: локально это localhost, в Docker — имя сервиса recommendations.
  * Каждый вызов с дедлайном 2 с. Ошибки gRPC превращаются в понятные HTTP-коды: INVALID_ARGUMENT → 400, недоступность сервиса → 503.

### Запуск
1. Создайте виртуальное окружение:
```sh
python -m venv env
```
2. Активируйте виртуальное окружение
3. Установите зависимости:
```sh
pip install -r marketplace/requirements.txt
pip install -r recommendations/requirements.txt
```
4. Сгенерируйте код для `.proto` файлов:
```sh
python generate_protos.py
```
5. Запустите сервис рекомендаций:
```sh
python recommendations/recommendations.py
```
6. Запустите веб-приложение
```
cd marketplace
python -m uvicorn marketplace:app --port 8000
```

### Выполенные задания
1. Добавьте в Marketplace параметр category для главной страницы.

**✅ Выполнено в коммите 63f7bbd3b1bb523482f48b765b7345abea13980a.**
```diff
--- a/Microservices/marketplace/marketplace.py
+++ b/Microservices/marketplace/marketplace.py
 CATEGORIES = {
     "science_fiction": BookCategory.BOOK_CATEGORY_SCIENCE_FICTION,
     "self_help": BookCategory.BOOK_CATEGORY_SELF_HELP,
 }
+CATEGORY_NAMES = {
+    "mystery": "Mistery",
+    "science_fiction": "Science Fiction",
+    "self_help": "Self Help"
+}
 
 
 class BookOut(BaseModel):
 async def fetch_recommendations(
     stub: RecommendationsStub, user_id: int, category: CategoryName, max_results: int
 ) -> list[BookOut]:
     request = RecommendationRequest(
-        user_id=user_id, category=CATEGORIES[category], max_results=max_results
+        user_id=user_id, category=CATEGORIES.get(category), max_results=max_results
     )
     try:
         response = await stub.Recommend(request, timeout=2.0)
 async def get_recommendations(
 
 
 @app.get("/", response_class=HTMLResponse, include_in_schema=False)
-async def homepage(request: Request) -> str:
+async def homepage(request: Request, category: str = "mystery") -> str:
     books = await fetch_recommendations(
-        request.app.state.recommendations, user_id=1, category="mystery", max_results=3
+        request.app.state.recommendations, user_id=1, category=category, max_results=3
     )
     items = "\n".join(f"      <li>{html.escape(book.title)}</li>" for book in books)
     return f"""<!doctype html>
 async def homepage(request: Request) -> str:
     <title>Online Books For You</title>
   </head>
   <body>
-    <h1>Mystery books you may like</h1>
+    <h1>{CATEGORY_NAMES.get(category)} books you may like</h1>
     <ul>
 {items}
     </ul>
```
2. Добавьте тест, проверяющий ответ 400 при ошибке INVALID_ARGUMENT от Recommendations.

**✅ Выполнено в коммите 0ab977a3d25611d83c25c4eb36720d3f0bb110ae.**
```diff
--- a/Microservices/marketplace/test_marketplace_integration.py
+++ b/Microservices/marketplace/test_marketplace_integration.py

 """Интеграционные тесты: нужны запущенные Marketplace и Recommendations."""
 import json
 import os
-from urllib.request import urlopen
+from urllib.request import urlopen, HTTPError
 
 BASE_URL = os.getenv("MARKETPLACE_URL", "http://localhost:8000")
 
 def test_homepage_renders_three_books():
     assert "<title>Online Books For You</title>" in page
     assert page.count("<li>") == 3
 
+def test_homepage_returns_400_on_invalid_argument():
+    try:
+        urlopen(f"{BASE_URL}?category=unknown_category", timeout=5)
+        raise RuntimeError("HTTPError was not raised!")
+    except HTTPError as e:
+        assert e.status == 400
 
 def test_api_returns_recommendations():
     url = f"{BASE_URL}/api/v1/recommendations?user_id=1&category=science_fiction&max_results=2"
```
3. Добавьте в RecommendationRequest поле repeated int32 exclude_ids = 4;, чтобы не рекомендовать уже прочитанные книги. Проверьте, что старый Marketplace (без перегенерации кода) продолжает работать с новым Recommendations.

**✅ Выполнено в коммите fc1a1e236eb0774062f67b8bd282b5f4ab731115.**
```diff
--- a/RPC/Microservices/marketplace/marketplace.py
+++ b/RPC/Microservices/marketplace/marketplace.py
 app = FastAPI(title="Marketplace", version="1.0.0", lifespan=lifespan)
 
 
 async def fetch_recommendations(
-    stub: RecommendationsStub, user_id: int, category: CategoryName, max_results: int
+    stub: RecommendationsStub, user_id: int, category: CategoryName, max_results: int,
+    exclude_ids: list[int] | None
 ) -> list[BookOut]:
     request = RecommendationRequest(
-        user_id=user_id, category=CATEGORIES.get(category), max_results=max_results
+        user_id=user_id, category=CATEGORIES.get(category), max_results=max_results,
+        exclude_ids=exclude_ids
     )
     try:
         response = await stub.Recommend(request, timeout=2.0)
 async def get_recommendations(
     user_id: int,
     category: CategoryName = "mystery",
     max_results: Annotated[int, Query(ge=1, le=10)] = 3,
+    exclude_id: Annotated[list[int] | None, Query()] = None,
 ) -> list[BookOut]:
     """Рекомендации книг выбранной категории."""
     return await fetch_recommendations(
-        request.app.state.recommendations, user_id, category, max_results
+        request.app.state.recommendations, user_id, category, max_results, exclude_ids=exclude_id
     )
 
 
 @app.get("/", response_class=HTMLResponse, include_in_schema=False)
-async def homepage(request: Request, category: str = "mystery") -> str:
+async def homepage(request: Request, category: str = "mystery", exclude_id: Annotated[list[int] | None, Query()] = None) -> str:
     books = await fetch_recommendations(
-        request.app.state.recommendations, user_id=1, category=category, max_results=3
+        request.app.state.recommendations, user_id=1, category=category, max_results=3,
+        exclude_ids=exclude_id
     )
     items = "\n".join(f"      <li>{html.escape(book.title)}</li>" for book in books)
     return f"""<!doctype html>
--- a/RPC/Microservices/protos/recommendations.proto
+++ b/RPC/Microservices/protos/recommendations.proto
 message RecommendationRequest {
   int32 user_id = 1;
   BookCategory category = 2;
   int32 max_results = 3;
+  repeated int32 exclude_ids = 4;
 }
 
 message BookRecommendation {
--- a/RPC/Microservices/recommendations/recommendations.py
+++ b/RPC/Microservices/recommendations/recommendations.py
 from concurrent import futures
 
 import grpc
 import recommendations_pb2_grpc
-from recommendations_pb2 import BookCategory, BookRecommendation, RecommendationResponse
+from recommendations_pb2 import BookCategory, BookRecommendation, RecommendationRequest, RecommendationResponse
 
 BOOKS_BY_CATEGORY = {
     BookCategory.BOOK_CATEGORY_MYSTERY: [
 BOOKS_BY_CATEGORY = {
 
 
 class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
-    def Recommend(self, request, context):
+    def Recommend(self, request: RecommendationRequest, context):
         if request.max_results <= 0:
             context.abort(grpc.StatusCode.INVALID_ARGUMENT, "max_results must be positive")
         if request.category == BookCategory.BOOK_CATEGORY_UNSPECIFIED:
 class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
         books = BOOKS_BY_CATEGORY.get(request.category)
         if books is None:
             context.abort(grpc.StatusCode.NOT_FOUND, f"Category {request.category} not found")
+            return
+        books = list(filter(lambda b: b.id not in request.exclude_ids, books))
         num_results = min(request.max_results, len(books))
-        return RecommendationResponse(recommendations=random.sample(books, num_results))
+        recommendations = random.sample(books, num_results)
+        return RecommendationResponse(recommendations=recommendations)
 
 
 def create_server(port: int = 50051) -> tuple[grpc.Server, int]:
```