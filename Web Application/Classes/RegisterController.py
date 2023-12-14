import pyodbc

# Метод для регистрации нового пользователя
def register_user(username: str, password: str, email: str) -> bool:
    try:
        # Строка подключения
        connection_string = 'DRIVER={SQL Server};SERVER=your_server_name;DATABASE=your_database_name;UID=your_username;PWD=your_password'
        
        # Установка соединения
        connection = pyodbc.connect(connection_string)

        # Создание объекта курсора
        cursor = connection.cursor()

        # SQL-запрос для вставки нового пользователя в таблицу
        insert_query = f"INSERT INTO Users (Username, Password, Email) VALUES ('{username}', '{password}', '{email}')"

        # Выполнение запроса
        cursor.execute(insert_query)

        # Подтверждение изменений в базе данных
        connection.commit()

        print("Пользователь успешно зарегистрирован.")
        return True

    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        return False

    finally:
        # Закрытие соединения
        if connection:
            connection.close()
