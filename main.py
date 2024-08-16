import mysql.connector
from pets_animals.dog import Dog
from pets_animals.cat import Cat
from pets_animals.hamster import Hamster
from counter import Counter

# Функция для получения подключения к базе данных
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # Адрес сервера MySQL
            user="root",    # Имя пользователя MySQL
            password="it123456789P.",# Пароль пользователя MySQL
            database="friends_of_man" # Название базы данных
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Ошибка подключения к базе данных: {err}")
        return None

# Функция для загрузки животных из базы данных
def load_animals():
    animals = []
    connection = get_db_connection()
    
    if connection is None:
        return animals  # Если подключение не удалось, возвращаем пустой список

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, owner, type FROM animals")
        rows = cursor.fetchall()

        # Отладочный вывод для проверки загруженных данных
        print("Загруженные строки из базы данных:", rows)

        for row in rows:
            animal = None
            if row['type'] == 'dog':
                animal = Dog(row['name'], row['owner'])
            elif row['type'] == 'cat':
                animal = Cat(row['name'], row['owner'])
            elif row['type'] == 'hamster':
                animal = Hamster(row['name'], row['owner'])

            if animal:
                animals.append(animal)

    except mysql.connector.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")
    
    finally:
        cursor.close()
        connection.close()

    return animals

# Функция для сохранения животных в базу данных
def save_animals(animals):
    connection = get_db_connection()
    
    if connection is None:
        print("Не удалось подключиться к базе данных для сохранения.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM animals")  # Очистка таблицы перед записью новых данных

        for animal in animals:
            cursor.execute(
                "INSERT INTO animals (name, owner, type) VALUES (%s, %s, %s)",
                (animal.name, animal.owner, animal.__class__.__name__.lower())
            )

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Ошибка при сохранении данных: {err}")
    
    finally:
        cursor.close()
        connection.close()

# Основная функция программы
def main():
    animals = load_animals()  # Загружаем животных из базы данных
    with Counter() as counter:
        while True:
            print("\nМеню:")
            print("1. Завести новое животное")
            print("2. Показать список животных")
            print("3. Обучить животное новой команде")
            print("4. Показать команды животного")
            print("5. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                name = input("Введите имя животного: ")
                owner = input("Введите имя владельца: ")
                animal_type = input("Введите тип животного (dog, cat, hamster): ").lower()

                if animal_type == 'dog':
                    animal = Dog(name, owner)
                elif animal_type == 'cat':
                    animal = Cat(name, owner)
                elif animal_type == 'hamster':
                    animal = Hamster(name, owner)
                else:
                    print("Неизвестный тип животного.")
                    continue

                animals.append(animal)
                counter.add()  # Увеличиваем счетчик
                print(f"{animal.name} успешно заведено!")
                save_animals(animals)  # Сохраняем животных в базу данных

            elif choice == '2':
                print("Список животных:")
                if animals:
                    for animal in animals:
                        print(f"- {animal.name} ({animal.__class__.__name__})")
                else:
                    print("Животных нет в базе данных.")

            elif choice == '3':
                name = input("Введите имя животного, которое хотите обучить: ")
                for animal in animals:
                    if animal.name == name:
                        command = input("Введите команду для обучения: ")
                        animal.add_command(command)
                        print(f"{animal.name} обучено новой команде: {command}")
                        break
                else:
                    print("Животное не найдено.")

            elif choice == '4':
                name = input("Введите имя животного, команды которого хотите увидеть: ")
                for animal in animals:
                    if animal.name == name:
                        commands = animal.get_commands()
                        print(f"Команды для {animal.name}: {commands}")
                        break
                else:
                    print("Животное не найдено.")

            elif choice == '5':
                print("Выход из программы.")
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

if __name__ == "__main__":
    main()