from datetime import datetime, timedelta  # Для работы с динамической датой
import random  # Чтобы делать случайные буквы
import string  # Чтобы взять английский алфавит

def generate_random_string(length=10):  # Функция создаёт случайную строку из букв
    letters = string.ascii_lowercase  
    return ''.join(random.choice(letters) for i in range(length))  

def generate_courier_data():  # Функция создаёт данные для нового курьера
    login = generate_random_string(10)  
    password = generate_random_string(10)  
    first_name = generate_random_string(10)  
    # Возвращаем словарь с данными
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d") # делаем завтрашнею дату в тесте
# Данные для заказа
BASE_ORDER_DATA = {
    "firstName": "Иван",
    "lastName": "Иванов",
    "address": "Москва, ул. Ленина, д. 10, кв. 25",
    "metroStation": 4,
    "phone": "+7 999 123 45 67",
    "rentTime": 5,
    "deliveryDate": tomorrow_date,
    "comment": "Позвонить за час до доставки"
}