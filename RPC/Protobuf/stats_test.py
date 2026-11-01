import time

import grpc

import stats_pb2
import stats_pb2_grpc
import stats_server

stats_grpc_server = stats_server.serve(port=50053)
stats_channel = grpc.insecure_channel("localhost:50053")
stats_stub = stats_pb2_grpc.StatsStub(stats_channel)
print("Сервер Stats запущен")

# Серверный поток: ответы приходят по мере готовности
start = time.monotonic()
for reply in stats_stub.Countdown(stats_pb2.CountdownRequest(start=5), timeout=10):
    print(f"{time.monotonic() - start:4.1f} с: {reply.value}")

# Клиентский поток: отправляем генератор, получаем один ответ
def numbers(values):
    for value in values:
        yield stats_pb2.Number(value=value)


summary = stats_stub.Sum(numbers([1, 2, 3.5, 10]), timeout=5)
print(f"Сумма {summary.total} из {summary.count} чисел")

# Двунаправленный поток: отправка и получение чередуются
def slow_numbers(values, delay=0.3):
    for value in values:
        print(f"  → отправляем {value}")
        yield stats_pb2.Number(value=value)
        time.sleep(delay)


for reply in stats_stub.RunningAverage(slow_numbers([10, 20, 30, 40]), timeout=10):
    print(f"  ← среднее после {reply.count} чисел: {reply.average}")

# Отмена потока клиентом и ошибка INVALID_ARGUMENT
responses = stats_stub.Countdown(stats_pb2.CountdownRequest(start=20), timeout=10)
try:
    for reply in responses:
        print(reply.value, end=" ")
        if reply.value == 17:
            responses.cancel()                  # больше не нужно
except grpc.RpcError as error:
    print("\nВызов завершён:", error.code())

try:
    list(stats_stub.Countdown(stats_pb2.CountdownRequest(start=-1), timeout=5))
except grpc.RpcError as error:
    print("Ошибка:", error.code(), "—", error.details())

stats_channel.close()
stats_grpc_server.stop(grace=None)
print("Сервер Stats остановлен")