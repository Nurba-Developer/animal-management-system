import json
from pets_animals.dog import Dog
from pets_animals.cat import Cat
from pets_animals.hamster import Hamster
from counter import Counter

DATA_FILE = 'animals.json'

def load_animals():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            animals = []
            for animal_data in data:
                animal = None  # Initialize animal to None
                if animal_data['type'] == 'собака':
                    animal = Dog(animal_data['name'], animal_data['owner'])
                elif animal_data['type'] == 'кошка':
                    animal = Cat(animal_data['name'], animal_data['owner'])
                elif animal_data['type'] == 'хомяк':
                    animal = Hamster(animal_data['name'], animal_data['owner'])
                
                if animal:  # Only append if animal is not None
                    animals.append(animal)
                else:
                    print(f"Неизвестный тип животного: {animal_data['type']}. Пропускаем.")

            return animals
    except FileNotFoundError:
        return []

def save_animals(animals):
    data = []
    for animal in animals:
        data.append({
            'name': animal.name,
            'owner': animal.owner,
            'type': animal.__class__.__name__.lower()
        })
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

def main():
    animals = load_animals()  # Загружаем животных из файла
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
                animal_type = input("Введите тип животного (собака, кошка, хомяк): ").lower()

                if animal_type == 'собака':
                    animal = Dog(name, owner)
                elif animal_type == 'кошка':
                    animal = Cat(name, owner)
                elif animal_type == 'хомяк':
                    animal = Hamster(name, owner)
                else:
                    print("Неизвестный тип животного.")
                    continue

                animals.append(animal)
                counter.add()  # Увеличиваем счетчик
                print(f"{animal.name} успешно заведено!")
                save_animals(animals)  # Сохраняем животных в файл

            elif choice == '2':
                print("Список животных:")
                for animal in animals:
                    print(f"- {animal.name} ({animal.__class__.__name__})")

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