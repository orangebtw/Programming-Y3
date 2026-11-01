import requests

response = requests.get(
    "http://127.0.0.1:8000/api/v1/recommendations",
    params={"user_id": 1, "category": "science_fiction", "max_results": 2},
    timeout=5,
)
print(response.status_code, response.json())

# Валидация FastAPI: max_results вне диапазона → 422
bad = requests.get("http://127.0.0.1:8000/api/v1/recommendations",
                   params={"user_id": 1, "max_results": 50}, timeout=5)
print(bad.status_code, bad.json()["detail"][0]["msg"])

print(requests.get("http://127.0.0.1:8000/", timeout=5).text)