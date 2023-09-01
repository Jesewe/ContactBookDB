import sqlite3
import os
from colorama import Fore, Style, init

init(autoreset=True)

def create_table_if_not_exists(connection):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Users (
        LastName TEXT,
        FirstName TEXT,
        MiddleName TEXT,
        PhoneNumber TEXT,
        Address TEXT
    )
    '''
    connection.execute(create_table_query)
    connection.commit()

def show_database(connection):
    os.system("cls" if os.name == "nt" else "clear")  # Очистка консоли
    print(Fore.YELLOW + "Содержимое базы данных:")
    select_query = "SELECT * FROM Users"
    cursor = connection.execute(select_query)
    for row in cursor:
        print(Fore.CYAN + "Фамилия:", row[0])
        print("Имя:", row[1])
        print("Отчество:", row[2])
        print("Номер Телефона:", row[3])
        print("Адрес:", row[4])
        print()

def search_in_database(connection, search_term):
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.MAGENTA + "Результаты поиска:")
    search_query = "SELECT * FROM Users WHERE LastName LIKE ?"
    cursor = connection.execute(search_query, ('%' + search_term + '%',))
    for row in cursor:
        print(Fore.CYAN + "Фамилия:", row[0])
        print("Имя:", row[1])
        print("Отчество:", row[2])
        print("Номер Телефона:", row[3])
        print("Адрес:", row[4])
        print()

def delete_from_database(connection, last_name):
    delete_query = "DELETE FROM Users WHERE LastName = ?"
    connection.execute(delete_query, (last_name,))
    connection.commit()
    print(Fore.GREEN + f"Пользователь с фамилией '{last_name}' удален из базы данных.")

def main():
    connection = sqlite3.connect("user_database.db")
    create_table_if_not_exists(connection)
    
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")  # Очистка консоли
            print("[1] Добавить пользователя")
            print("[2] Показать базу данных")
            print("[3] Удалить пользователя")
            print("[4] Поиск пользователя по фамилии")
            print("[5] Выйти")
            
            choice = input("\nВведите номер выбранного действия: ")
            
            if choice == "1":
                os.system("cls" if os.name == "nt" else "clear")
                print(Fore.MAGENTA + "Введите данные пользователя:")
                last_name = input("Фамилия: ")
                first_name = input("Имя: ")
                middle_name = input("Отчество: ")
                phone_number = input("Номер Телефона: ")
                address = input("Адрес: ")
                
                insert_query = "INSERT INTO Users (LastName, FirstName, MiddleName, PhoneNumber, Address) VALUES (?, ?, ?, ?, ?)"
                connection.execute(insert_query, (last_name, first_name, middle_name, phone_number, address))
                connection.commit()
                
                print(Fore.GREEN + "Пользователь успешно добавлен в базу данных.")
            
            elif choice == "2":
                show_database(connection)
                input(Fore.CYAN + "Нажмите Enter, чтобы продолжить...")
            
            elif choice == "3":
                os.system("cls" if os.name == "nt" else "clear")
                last_name_to_delete = input("Введите фамилию пользователя для удаления: ")
                delete_from_database(connection, last_name_to_delete)
                input(Fore.CYAN + "Нажмите Enter, чтобы продолжить...")
            
            elif choice == "4":
                os.system("cls" if os.name == "nt" else "clear")
                search_term = input("Введите часть фамилии для поиска: ")
                search_in_database(connection, search_term)
                input(Fore.CYAN + "Нажмите Enter, чтобы продолжить...")

            elif choice == "5":
                break
            
            else:
                print(Fore.RED + "Неверный выбор. Пожалуйста, выберите действие из списка.")
                input(Fore.CYAN + "Нажмите Enter, чтобы продолжить...")
                
    except Exception as ex:
        print(Fore.RED + "Произошла ошибка:", ex)
    finally:
        connection.close()
        print(Fore.YELLOW + "Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()