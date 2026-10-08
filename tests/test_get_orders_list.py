import allure # Импортируем библиотеку для отчётов
from order_api import OrderApi # Импортируем класс для работы с ручками заказа

class TestGetOrdersList: # Класс для тестов получения списка заказов

    @allure.title("Получение списка заказов возвращает массив заказов")
    def test_get_orders_list_success(self): # Тест на получение списка заказов
        order_api = OrderApi()
        response = order_api.get_orders_list()
        assert response.status_code == 200 # Проверяем код 200
        assert "orders" in response.json() # Проверяем наличие ключа orders в ответе
        assert isinstance(response.json()["orders"], list) # Проверяем, что orders является списком