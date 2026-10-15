import pytest  # Импортируем библиотеку для тестирования
from courier_api import CourierApi  # Импортируем класс для работы с ручками курьера
from generators import generate_courier_data  # Импортируем функцию для генератора данных курьера

@pytest.fixture  # Фикстура для автоматического удаления курьера после теста
def delete_courier_after_test():
    created_couriers = []

    def _register(payload, api_client):  # регистрируем курьера для удаления после теста
        created_couriers.append((payload, api_client))  # Добавляем данные курьера и клиента в список на удаление
    yield _register  # Передаем функцию-регистратор в тест для использования во время выполнения

    for payload, api_client in created_couriers:  # После теста удаляем всех зарегистрированных курьеров
        login_res = api_client.login_courier({"login": payload["login"], "password": payload["password"]})  # логинимся, чтобы получить id курьера для удаления 
        if login_res.status_code == 200:
            courier_id = login_res.json().get("id")
            if courier_id is not None:
                api_client.delete_courier(courier_id)

@pytest.fixture  # Фикстура для создания курьера перед тестом и удаления после завершения
def courier_create_and_delete(delete_courier_after_test):
    courier_api = CourierApi()
    payload = generate_courier_data()
    response = courier_api.create_courier(payload)  # Создаем курьера через API без assert
    delete_courier_after_test(payload, courier_api)  # Регистрируем курьера для автоматического удаления
    yield payload, courier_api  # Передаем данные курьера и API в тест