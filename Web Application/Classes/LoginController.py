import pyodbc

# Метод для логирования пользователя
def login_user(username: str, password: str) -> bool:
    try:
        # Строка подключения
        connection_string = 'DRIVER={SQL Server};SERVER=your_server_name;DATABASE=your_database_name;UID=your_username;PWD=your_password'
        
        # Установка соединения
        connection = pyodbc.connect(connection_string)

        # Создание объекта курсора
        cursor = connection.cursor()

        # SQL-запрос для проверки учетных данных пользователя
        select_query = f"SELECT * FROM Users WHERE Username = '{username}' AND Password = '{password}'"

        # Выполнение запроса
        cursor.execute(select_query)

        # Получение результата
        user = cursor.fetchone()

        if user:
            print("Пользователь успешно вошел в систему.")
            return True
        else:
            print("Неверные учетные данные. Вход в систему не выполнен.")
            return False

    except Exception as e:
        print(f"Ошибка при входе пользователя: {e}")
        return False

    finally:
        # Закрытие соединения
        if connection:
            connection.close()