# URL учебного сервиса Яндекс Самокат
BASE_URL = "https://qa-scooter.praktikum-services.ru"
# Ручки для работы с курьерами 
CREATE_COURIER_URL = f"{BASE_URL}/api/v1/courier"        # POST — Создание курьера
LOGIN_COURIER_URL = f"{BASE_URL}/api/v1/courier/login"   # POST — Логин курьера
DELETE_COURIER_URL = f"{BASE_URL}/api/v1/courier/"       # DELETE — Удаление курьера (к URL прибавляем id)
# Ручки для работы с заказами 
CREATE_ORDER_URL = f"{BASE_URL}/api/v1/orders"          # POST — Создание заказа
GET_ORDERS_URL = f"{BASE_URL}/api/v1/orders"            # GET — Получение списка заказов