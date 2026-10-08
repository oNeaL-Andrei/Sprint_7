import allure  # Импортируем библиотеку для отчётов
import pytest  # Импортируем библиотеку для тестирования

from data import BASE_ORDER_DATA  # Базовые данные заказа
from order_api import OrderApi  # Класс работы с ручками заказов

class TestCreateOrder:  # Класс для тестов создания заказа
    @pytest.mark.parametrize("color", [
        ["BLACK"],            # Только черный цвет
        ["GREY"],             # Только серый цвет
        ["BLACK", "GREY"],    # Оба цвета
        []                    # Без указания цвета
    ])
    @allure.title("Создание заказа с разным набором цветов возвращает track")
    def test_create_order_with_different_colors_returns_track(self, color):  # Тест создания заказа
        order_api = OrderApi()
        payload = BASE_ORDER_DATA.copy()  # Копируем словарь с базовыми данными
        if color:
            payload["color"] = color  # Добавляем цвет
        response = order_api.create_order(payload) # Отправляем POST-запрос на создание заказа

        assert response.status_code == 201  # Проверяем код 201
        assert "track" in response.json()  # Проверяем наличия трек-номера в ответе