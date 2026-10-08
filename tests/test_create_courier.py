import allure  # Импортируем библиотеку для отчётов
import pytest  # Импортируем библиотеку для тестирования
from courier_api import CourierApi  # Импортируем класс для работы с ручками курьера
from data import generate_courier_data  # Импортируем функцию для генерации данных курьера

class TestCreateCourier:  # Класс для тестов создания курьера

    @allure.title("Создание курьера")
    def test_create_courier_success(self):  # Тест на успешное создание курьера
        courier_api = CourierApi()
        payload = generate_courier_data()
        response = courier_api.create_courier(payload) 
        assert response.status_code == 201 
        assert response.json() == {"ok": True}

        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]}) # Очистка данных после теста
        if login_res.status_code == 200:
            courier_id = login_res.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title("Успешное создание курьера без необязательного поля firstName")
    def test_create_courier_without_first_name_success(self):  # Тест на создание курьера без firstName
        courier_api = CourierApi()
        payload = generate_courier_data()
        payload.pop("firstName")  # Удаляем необязательное поле

        response = courier_api.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]}) # Очистка данных после теста
        if login_res.status_code == 200:
            courier_id = login_res.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_error(self):  # Тест на создание двух одинаковых курьеров
        courier_api = CourierApi()
        payload = generate_courier_data()
        courier_api.create_courier(payload)  # Создаем первого курьера

        response = courier_api.create_courier(payload)  # Пробуем создать второго с такими же данными

        assert response.status_code == 409  # Проверяем код и текст ошибки
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]}) # Очистка данных после теста
        if login_res.status_code == 200:
            courier_id = login_res.json().get("id")
            courier_api.delete_courier(courier_id)

    @pytest.mark.parametrize("missing_field", ["login", "password"])  # Параметризуем тест на создание курьера без обязательного поля
    @allure.title("Ошибка при создании курьера без обязательного поля")
    def test_create_courier_without_required_field_error(self, missing_field):  # Тест на создание курьера без обязательного поля
        courier_api = CourierApi()
        payload = generate_courier_data()

        payload.pop(missing_field)  # Удаляем одно из обязательных полей

        response = courier_api.create_courier(payload)

        assert response.status_code == 400  # Проверяем код и текст ошибки
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"