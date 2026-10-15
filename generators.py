from datetime import datetime, timedelta  # Для работы с датой
import random  # Импортируем модуль random для генерации случайных значений
import string  # Импортируем модуль string для работы с буквами

def generate_random_string(length=10):  # Функция создаёт случайную строку из букв
    letters = string.ascii_lowercase  
    return ''.join(random.choice(letters) for i in range(length))  

def generate_courier_data():  # Функция создаёт данные для нового курьера
    login = generate_random_string(10)  
    password = generate_random_string(10)  
    first_name = generate_random_string(10)  
    return {"login": login,"password": password,"firstName": first_name}  # Возвращаем словарь с данными

def generate_delivery_date():  # делаем завтрашнею дату в тесте
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")