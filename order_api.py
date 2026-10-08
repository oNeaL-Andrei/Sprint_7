import requests  # Импортируем библиотеку для отправки запросов
import urls  # Импортируем файл с адресами

class OrderApi: # Класс для работы с ручками заказов

    def create_order(self, payload): # Метод для создания заказа (POST-запрос)
        return requests.post(urls.CREATE_ORDER_URL, json=payload)

    def get_orders_list(self): # Метод для получения списка заказов (GET-запрос)
        return requests.get(urls.GET_ORDERS_URL)