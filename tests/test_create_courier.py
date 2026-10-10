import allure  # Импортируем библиотеку для отчётов
import pytest  # Импортируем библиотеку для тестирования
from courier_api import CourierApi  # Импортируем класс для работы с ручками курьера
from generators import generate_courier_data  # Импортируем функцию для генерации данных курьера

class TestCreateCourier:  # Класс для тестов создания курьера

    @allure.title("Создание курьера")
    def test_create_courier_success(self, delete_courier_after_test):  # Тест на успешное создание курьера
        courier_api = CourierApi()
        payload = generate_courier_data()
        delete_courier_after_test(payload, courier_api)  # Регистрируем курьера на автоматическое удаление через фикстуру
        response = courier_api.create_courier(payload)  # Создаем курьера через API

        assert response.status_code == 201  # Проверяем код ответа 201
        assert response.json() == {"ok": True}  # Проверяем успешное тело ответа

    @allure.title("Успешное создание курьера без необязательного поля firstName")
    def test_create_courier_without_first_name_success(self, delete_courier_after_test):  # Тест на создание курьера без необязательного поля
        courier_api = CourierApi()  # Создаём экзенпляр класса
        payload = generate_courier_data()  # генерируем данные курьера
        payload.pop("firstName")  # Удаляем необязательное поле
        delete_courier_after_test(payload, courier_api)  # Регистрируем курьера на автоматическое удаление через фикстуру
        response = courier_api.create_courier(payload)  # Создаем курьера без firstName

        assert response.status_code == 201  # Проверяем код ответа 201
        assert response.json() == {"ok": True}  # Проверяем успешное тело ответа

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_error(self, courier_create_and_delete):  # Тест на создание двух одинаковых курьеров
        payload, courier_api = courier_create_and_delete  # Используем фикстуру для создания курьера и его последующего удаления
        response = courier_api.create_courier(payload)  # Пробуем создать второго с такими же данными

        assert response.status_code == 409  # Проверяем код ошибки 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."  # Проверяем текст ошибки

    @pytest.mark.parametrize("missing_field", ["login", "password"])  # Параметризуем тест на создание курьера без обязательного поля
    @allure.title("Ошибка при создании курьера без обязательного поля")
    def test_create_courier_without_required_field_error(self, missing_field):  # Тест на создание курьера без обязательного поля
        courier_api = CourierApi()
        payload = generate_courier_data()
        payload.pop(missing_field)  # Удаляем одно из обязательных полей
        response = courier_api.create_courier(payload)  # Отправляем запрос без обязательного поля

        assert response.status_code == 400  # Проверяем код ошибки 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"  # Проверяем текст ошибки