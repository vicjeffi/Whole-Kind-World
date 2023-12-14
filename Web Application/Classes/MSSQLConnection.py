import pyodbc

def connect_to_database(server: str, database: str, username: str, password: str) -> pyodbc.Connection:
    try:
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        connection = pyodbc.connect(connection_string)

        print("Успешное подключение к базе данных на MS SQL Server")
        return connection

    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None