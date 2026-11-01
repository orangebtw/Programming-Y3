# Программирование. Лабораторная работа «RPC. gRPC. Protobuf»

### Структура папок
* Microservices -- Приложение Marketplace на FastAPI
* Protobuf -- Знакомство с Protocol Buffers

## Protobuf
...

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
uvicorn marketplace:app --port 8000
```

### Выполенные задания
1. **Добавьте в Marketplace параметр category для главной страницы**.
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