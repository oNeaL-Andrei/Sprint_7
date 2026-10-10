import allure  # Для отчётов Allure
import pytest  # Для параметризации
from courier_api import CourierApi  # Импортируем класс для работы с ручками курьера
from generators import generate_courier_data  # Импортируем функцию для генерации данных курьера

class TestLoginCourier:  # Класс для тестов логина курьера

    @allure.title("Курьер может успешно авторизоваться и получить id")
    def test_login_courier_success(self, courier_create_and_delete):  # Тест на успешный логин курьера
        payload, courier_api = courier_create_and_delete  # Используем фикстуру для создания и удаления курьера
        login_payload = {"login": payload["login"], "password": payload["password"]}
        response = courier_api.login_courier(login_payload)

        assert response.status_code == 200  # Проверяем код 200
        assert "id" in response.json()  # Проверяем наличие id в ответе

    @pytest.mark.parametrize("field", ["login", "password"])  # Параметризуем тест на логин курьера без одного из обязательных полей
    @allure.title("Ошибка при авторизации без одного из обязательных полей")
    def test_login_courier_without_field_error(self, field, courier_create_and_delete):  # Тест на логин курьера без одного из обязательных полей
        payload, courier_api = courier_create_and_delete  # Используем фикстуру для создания и удаления курьера
        login_payload = {"login": payload["login"], "password": payload["password"]}  # Создаём словырь с данными для логина
        login_payload.pop(field)  # Удаляем обязательное поле
        response = courier_api.login_courier(login_payload)  # Отправляем POST-запрос на логин курьера без одного из обязательных полей

        assert response.status_code == 400  # Проверяем код 400
        assert response.json()["message"] == "Недостаточно данных для входа"  # Проверяем текст ошибки

    @pytest.mark.parametrize("incorrect_field, incorrect_prefix", [("login", "incorrect_"),("password", "incorrect_")])  # Проверяем неправильный логин и неправильный пароль через параметризацию без условий
    @allure.title("Ошибка при авторизации с неправильным логином или паролем")
    def test_login_courier_with_incorrect_credentials(self, incorrect_field, incorrect_prefix, courier_create_and_delete):  # Тест на логин с неправильными данными
        payload, courier_api = courier_create_and_delete  # Используем фикстуру для создания и удаления курьера
        login_payload = {"login": payload["login"], "password": payload["password"]}  # Создаём словарь с данными для логина
        login_payload[incorrect_field] = incorrect_prefix + payload[incorrect_field]  # Изменяем одно из обязательных полей на неправильное значение
        response = courier_api.login_courier(login_payload)  # Отправляем POST- запрос 

        assert response.status_code == 404  # Проверяем код ошибки
        assert response.json()["message"] == "Учетная запись не найдена"  # Проверяем текст ошибки

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_non_existent_courier_error(self):  # Тест на логин несуществующего курьера
        courier_api = CourierApi()  # Создаём экземпляр с классами
        non_existent_payload = generate_courier_data()  # Генерируем случайные данные для несуществующего пользователя

        login_payload = {"login": non_existent_payload["login"], "password": non_existent_payload["password"]}  # Создаём словарь
        response = courier_api.login_courier(login_payload)  # Отправляем POST-запрос

        assert response.status_code == 404  # Проверяем код ошибки
        assert response.json()["message"] == "Учетная запись не найдена"  # Проверяем текст ошибки