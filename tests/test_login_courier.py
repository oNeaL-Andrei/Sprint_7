import allure  # Для отчётов Allure
import pytest  # Для параметризации
from courier_api import CourierApi  # Импортируем класс для работы с ручками курьера
from data import generate_courier_data  # Импортируем функцию для генерации данных курьера

class TestLoginCourier:  # Класс для тестов логина курьера

    @allure.title("Курьер может успешно авторизоваться и получить id")
    def test_login_courier_success(self):  # Тест на успешный логин курьера
        courier_api = CourierApi()
        payload = generate_courier_data()
        courier_api.create_courier(payload)
        login_payload = {"login": payload["login"], "password": payload["password"]}
        response = courier_api.login_courier(login_payload)

        assert response.status_code == 200  # Проверяем код 200
        assert "id" in response.json()  # Проверяем наличие id в ответе

        courier_id = response.json().get("id")
        courier_api.delete_courier(courier_id)  # Удаляем созданного курьера после теста

    @pytest.mark.parametrize("field", ["login", "password"])  # Параметризуем тест на логин курьера без одного из обязательных полей
    @allure.title("Ошибка при авторизации без одного из обязательных полей")
    def test_login_courier_without_field_error(self, field):  # Тест на логин курьера без одного из обязательных полей
        courier_api = CourierApi()
        payload = generate_courier_data()
        courier_api.create_courier(payload)
        login_payload = {"login": payload["login"], "password": payload["password"]}
        login_payload.pop(field)
        response = courier_api.login_courier(login_payload)

        assert response.status_code == 400  # Проверяем код 400
        assert response.json()["message"] == "Недостаточно данных для входа"  # Проверяем текст ошибки

        clean_login = courier_api.login_courier({"login": payload["login"], "password": payload["password"]})  # Очистка данных после теста
        if clean_login.status_code == 200:
            courier_api.delete_courier(clean_login.json().get("id"))

    @pytest.mark.parametrize("incorrect_field", ["login", "password"])  # Проверяем неправильный логин и неправильный пароль
    @allure.title("Ошибка при авторизации с неправильным логином или паролем")
    def test_login_courier_with_incorrect_credentials(self, incorrect_field):  # Тест на логин с неправильными данными
        courier_api = CourierApi()
        payload = generate_courier_data()
        courier_api.create_courier(payload)
        login_payload = {"login": payload["login"], "password": payload["password"]}
        if incorrect_field == "login":
            login_payload["login"] = "incorrect_" + payload["login"]
        else:
            login_payload["password"] = "incorrect_" + payload["password"]
        response = courier_api.login_courier(login_payload)

        assert response.status_code == 404  # Проверяем код ошибки
        assert response.json()["message"] == "Учетная запись не найдена"  # Проверяем текст ошибки

        clean_login = courier_api.login_courier({"login": payload["login"], "password": payload["password"]})  # Очистка данных после теста
        if clean_login.status_code == 200:
            courier_api.delete_courier(clean_login.json().get("id"))

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_non_existent_courier_error(self):  # Тест на логин несуществующего курьера
        courier_api = CourierApi()

        login_payload = {"login": "user_01", "password": "password"}
        response = courier_api.login_courier(login_payload)

        assert response.status_code == 404  # Проверяем код ошибки
        assert response.json()["message"] == "Учетная запись не найдена"  # Проверяем текст ошибки