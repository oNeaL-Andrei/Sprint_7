import allure  # Импортируем библиотеку для отчётов Allure
import requests  # Импортируем библиотеку для отправки запросов
import urls  # Импортируем файл с адресами

class CourierApi:  # Класс для работы с ручками курьера
   
    @allure.step("Создать курьера")
    def create_courier(self, payload):  # Метод для создания курьера (POST-запрос)
        return requests.post(urls.CREATE_COURIER_URL, json=payload)
    
    @allure.step("Авторизовать курьера в системе")
    def login_courier(self, payload):  # Метод для логина курьера (POST-запрос)
        return requests.post(urls.LOGIN_COURIER_URL, json=payload)

    @allure.step("Удалить курьера по ID")
    def delete_courier(self, courier_id):  # Метод для удаления курьера (DELETE-запрос)
        return requests.delete(f"{urls.DELETE_COURIER_URL}{courier_id}")