# -*- coding: utf-8 -*-
"""
==============================================
 ГЛАВНЫЙ ФАЙЛ ПРИЛОЖЕНИЯ
 Менеджер паролей с генерацией паролей
==============================================
"""

import os
import json
import logging
import sys
import io

# Настраиваем кодировку для Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

from password_generator import PasswordGenerator
from password_store import PasswordStore

# ==========================================
# НАСТРОЙКА ЛОГИРОВАНИЯ
# ==========================================

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# ==========================================
# ПРОВЕРКА ПОХОЖИХ СИМВОЛОВ
# ==========================================

# Символы, которые легко перепутать
SIMILAR_CHARS = {
    '0': 'ноль (похоже на O)',
    'O': 'буква О (похоже на 0)',
    'o': 'строчная о (похоже на 0)',
    'l': 'строчная Л (похоже на 1 или I)',
    'I': 'заглавная I (похоже на l)',
    'i': 'строчная i (похоже на l)',
    '1': 'единица (похоже на l)',
    '|': 'вертикальная черта (похоже на l или I)',
}


def check_similar_chars(password):
    """Проверить пароль на похожие символы."""
    found = []
    for char in password:
        if char in SIMILAR_CHARS:
            found.append(f"'{char}' — {SIMILAR_CHARS[char]}")
    return found


# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================

def show_main_menu():
    """Показать главное меню."""
    print("\n" + "=" * 50)
    print("  МЕНЕДЖЕР ПАРОЛЕЙ С ГЕНЕРАТОРОМ")
    print("=" * 50)
    print("  1. Показать все записи")
    print("  2. Добавить новую запись")
    print("  3. Изменить пароль записи")
    print("  4. Найти запись")
    print("  5. Удалить запись")
    print("  6. Сгенерировать пароль")
    print("  7. Статистика")
    print("  8. Выход")
    print("=" * 50)


# ==========================================
# ПОКАЗ ВСЕХ ЗАПИСЕЙ
# ==========================================

def show_all_records(store):
    """Показать все записи."""
    print("\n" + "-" * 50)
    print("  ВСЕ ЗАПИСИ:")
    print("-" * 50)

    records = store.get_all_records()

    if not records:
        print("  Записей пока нет.")
        return

    for i, record in enumerate(records, 1):
        print(f"  {i}. {record['name']}")
        print(f"     Логин: {record['login']}")
        print(f"     Пароль: {'*' * len(record['password'])}")
        print()

    print("-" * 50)
    print(f"  Всего записей: {len(records)}")
    print("-" * 50)


# ==========================================
# ДОБАВЛЕНИЕ ЗАПИСИ
# ==========================================

def add_new_record(store, generator):
    """Добавить новую запись."""
    print("\n" + "-" * 50)
    print("  ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ:")
    print("-" * 50)

    try:
        name = input("  Название сервиса: ").strip()
        if not name:
            print("  Ошибка: название не может быть пустым!")
            return

        # Проверяем уникальность - сравниваем напрямую
        all_records = store.get_all_records()
        for record in all_records:
            if record['name'].lower() == name.lower():
                print(f"\n  ЗАПРЕТ! Запись '{name}' уже существует!")
                print(f"  Удалите старую запись или используйте другое название.")
                return

        login = input("  Логин или email: ").strip()
        if not login:
            print("  Ошибка: логин не может быть пустым!")
            return

        print("\n  Как создать пароль?")
        print("  1. Сгенерировать автоматически (рекомендуется)")
        print("  2. Ввести свой пароль")

        choice = input("  Ваш выбор (1/2): ").strip()

        if choice == "1":
            print("\n  Настройки генерации:")
            length_input = input("  Длина пароля (по умолчанию 16): ").strip()
            length = int(length_input) if length_input.isdigit() else 16

            exclude_similar = input("  Исключить похожие (0/O, l/I)? (да/нет, по умолчанию да): ").strip().lower()
            exclude_similar = exclude_similar != "нет"

            use_special = input("  Спецсимволы (!@#$%...)? (да/нет, по умолчанию да): ").strip().lower()
            use_special = use_special != "нет"

            password = generator.generate(length=length, exclude_similar=exclude_similar, use_special=use_special)
            print(f"\n  Сгенерированный пароль: {password}")

        elif choice == "2":
            print("\n  ПАРАМЕТРЫ БЕЗОПАСНОГО ПАРОЛЯ:")
            print("  - Минимум 8 символов")
            print("  - Буквы + цифры + спецсимволы")
            print("  - ЗАПРЕЩЕНЫ похожие символы: 0, O, l, I, 1")
            print()
            password = input("  Введите пароль: ").strip()

            if not password:
                print("  Ошибка: пароль не может быть пустым!")
                return

            # ПРОВЕРКА ПОХОЖИХ СИМВОЛОВ
            found_similar = check_similar_chars(password)

            if found_similar:
                print()
                print("  ОШИБКА! Обнаружены похожие символы:")
                for s in found_similar:
                    print(f"    - {s}")
                print()
                print("  ПРИЧИНА: такие символы легко перепутать при вводе.")
                print()
                print("  РЕШЕНИЕ:")
                print("  1. Используйте генератор (пункт 1)")
                print("  2. Замените похожие символы:")
                print("     0 -> 2-9 | O -> A,B,C | l -> k,m,n | I -> H,J,K | 1 -> 2-9")
                return

            if len(password) < 4:
                print("  Ошибка: минимум 4 символа!")
                return

        else:
            print("  Неверный выбор!")
            return

        # Сохраняем
        success = store.add_record(name, login, password)

        if success:
            print(f"\n  Запись '{name}' добавлена!")
            strength = generator.check_password_strength(password)
            print(f"  Оценка: {strength['level']}")
            if strength['feedback']:
                print("  Рекомендации:")
                for tip in strength['feedback']:
                    print(f"    - {tip}")
        else:
            print("\n  Ошибка сохранения!")

    except Exception as e:
        print(f"  Ошибка: {e}")
        logger.error(f"Ошибка: {e}")


# ==========================================
# ИЗМЕНЕНИЕ ПАРОЛЯ
# ==========================================

def change_password(store, generator):
    """Изменить пароль существующей записи."""
    print("\n" + "-" * 50)
    print("  ИЗМЕНЕНИЕ ПАРОЛЯ:")
    print("-" * 50)

    records = store.get_all_records()

    if not records:
        print("  Нет записей для изменения.")
        return

    # Показываем список
    for i, record in enumerate(records, 1):
        print(f"  {i}. {record['name']} ({record['login']})")

    try:
        num_input = input("\n  Введите номер записи: ").strip()
        if not num_input.isdigit():
            print("  Ошибка: введите число!")
            return

        num = int(num_input) - 1
        if num < 0 or num >= len(records):
            print("  Ошибка: неверный номер!")
            return

        record = records[num]
        print(f"\n  Запись: {record['name']}")
        print(f"  Логин: {record['login']}")
        print(f"  Текущий пароль: {'*' * len(record['password'])}")

        print("\n  Новый пароль:")
        print("  1. Сгенерировать автоматически")
        print("  2. Ввести свой")

        choice = input("  Ваш выбор (1/2): ").strip()

        if choice == "1":
            length_input = input("  Длина (по умолчанию 16): ").strip()
            length = int(length_input) if length_input.isdigit() else 16
            password = generator.generate(length=length, exclude_similar=True, use_special=True)
            print(f"\n  Новый пароль: {password}")

        elif choice == "2":
            password = input("  Введите новый пароль: ").strip()

            if not password:
                print("  Ошибка: пароль не может быть пустым!")
                return

            found_similar = check_similar_chars(password)
            if found_similar:
                print("\n  ОШИБКА! Похожие символы:")
                for s in found_similar:
                    print(f"    - {s}")
                print("  Замените их или используйте генератор.")
                return

        else:
            print("  Неверный выбор!")
            return

        # Сохраняем
        success = store.update_record(record['name'], new_password=password)

        if success:
            print(f"\n  Пароль для '{record['name']}' обновлён!")
        else:
            print("\n  Ошибка обновления!")

    except Exception as e:
        print(f"  Ошибка: {e}")
        logger.error(f"Ошибка: {e}")


# ==========================================
# ПОИСК ЗАПИСИ
# ==========================================

def search_record(store):
    """Найти запись."""
    print("\n" + "-" * 50)
    print("  ПОИСК ЗАПИСИ:")
    print("-" * 50)

    query = input("  Введите название: ").strip()
    if not query:
        print("  Ошибка: введите запрос!")
        return

    results = store.search_records(query)

    if not results:
        print(f"  Записи '{query}' не найдены.")
        return

    print(f"\n  Найдено: {len(results)}")
    for record in results:
        print(f"  {record['name']}")
        print(f"    Логин: {record['login']}")
        print(f"    Пароль: {record['password']}")
        print()


# ==========================================
# УДАЛЕНИЕ ЗАПИСИ
# ==========================================

def delete_record(store):
    """Удалить запись."""
    print("\n" + "-" * 50)
    print("  УДАЛЕНИЕ ЗАПИСИ:")
    print("-" * 50)

    records = store.get_all_records()
    if not records:
        print("  Нет записей.")
        return

    for i, record in enumerate(records, 1):
        print(f"  {i}. {record['name']}")

    try:
        num_input = input("\n  Номер для удаления: ").strip()
        if not num_input.isdigit():
            print("  Ошибка: введите число!")
            return

        num = int(num_input) - 1
        if num < 0 or num >= len(records):
            print("  Ошибка: неверный номер!")
            return

        record = records[num]
        confirm = input(f"  Удалить '{record['name']}'? (да/нет): ").strip().lower()

        if confirm == "да":
            success = store.delete_record(record['name'])
            if success:
                print(f"  Запись '{record['name']}' удалена!")
            else:
                print("  Ошибка удаления!")
        else:
            print("  Отменено.")

    except Exception as e:
        print(f"  Ошибка: {e}")


# ==========================================
# ГЕНЕРАТОР ПАРОЛЕЙ
# ==========================================

def generate_password_menu(generator):
    """Генератор паролей."""
    print("\n" + "-" * 50)
    print("  ГЕНЕРАТОР ПАРОЛЕЙ:")
    print("-" * 50)

    try:
        length_input = input("  Длина (по умолчанию 16): ").strip()
        length = int(length_input) if length_input.isdigit() else 16

        exclude_similar = input("  Исключить похожие (да/нет, по умолчанию да): ").strip().lower()
        exclude_similar = exclude_similar != "нет"

        use_special = input("  Спецсимволы (да/нет, по умолчанию да): ").strip().lower()
        use_special = use_special != "нет"

        count_input = input("  Сколько паролей (по умолчанию 1): ").strip()
        count = int(count_input) if count_input.isdigit() else 1

        print("\n" + "=" * 50)
        print("  СГЕНЕРИРОВАННЫЕ ПАРОЛИ:")
        print("=" * 50)

        for i in range(count):
            password = generator.generate(length=length, exclude_similar=exclude_similar, use_special=use_special)
            print(f"  {i + 1}. {password}")

        print("=" * 50)

    except Exception as e:
        print(f"  Ошибка: {e}")


# ==========================================
# СТАТИСТИКА
# ==========================================

def show_statistics(store):
    """Показать статистику."""
    print("\n" + "-" * 50)
    print("  СТАТИСТИКА:")
    print("-" * 50)

    stats = store.get_statistics()
    print(f"  Всего записей: {stats['total_records']}")
    print(f"  Размер файла: {stats['file_size']} байт")
    print(f"  Последнее обновление: {stats['last_modified']}")
    print("-" * 50)


# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================

def main():
    """Главная функция приложения."""
    print("\n" + "*" * 50)
    print("  Добро пожаловать в Менеджер паролей!")
    print("  Безопасное хранение и генерация паролей")
    print("*" * 50)

    try:
        generator = PasswordGenerator()
        store = PasswordStore()

        # Добавляем тестовые записи
        if store.get_statistics()['total_records'] == 0:
            print("\n  Добавляем тестовые записи...")
            store.add_record("Gmail", "user@gmail.com", "MySecurePass123!")
            store.add_record("Telegram", "@username", "TelegramPass456!")
            print("  Готово: Gmail и Telegram")

        while True:
            show_main_menu()
            choice = input("\n  Ваш выбор (1-8): ").strip()

            if choice == "1":
                show_all_records(store)
            elif choice == "2":
                add_new_record(store, generator)
            elif choice == "3":
                change_password(store, generator)
            elif choice == "4":
                search_record(store)
            elif choice == "5":
                delete_record(store)
            elif choice == "6":
                generate_password_menu(generator)
            elif choice == "7":
                show_statistics(store)
            elif choice == "8":
                print("\n  До свидания! Ваши пароли в безопасности.")
                break
            else:
                print("\n  Неверный выбор! Введите число от 1 до 8.")

    except KeyboardInterrupt:
        print("\n\n  Программа завершена.")
    except Exception as e:
        print(f"\n  Критическая ошибка: {e}")
        logger.critical(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
