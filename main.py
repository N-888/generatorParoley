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
    """Добавить новую запись с жёсткими проверками."""
    print("\n" + "-" * 50)
    print("  ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ:")
    print("-" * 50)

    # ==========================================
    # ЭТАП 1: НАЗВАНИЕ СЕРВИСА
    # ==========================================
    while True:
        name = input("  Название сервиса (Gmail, Telegram...): ").strip()

        # Проверка на пустое название
        if not name:
            print("  [ОШИБКА] Название не может быть пустым!")
            print("  [ПОДСКАЗКА] Введите: Gmail, Telegram, VK и т.д.")
            logger.warning("Попытка создания записи с пустым названием")
            continue

        # Проверка на слишком короткое название
        if len(name) < 2:
            print("  [ОШИБКА] Название слишком короткое (минимум 2 символа)!")
            continue

        # Проверка на уникальность
        all_records = store.get_all_records()
        name_exists = False
        for record in all_records:
            if record['name'].lower() == name.lower():
                print(f"  [ОШИБКА] Запись '{name}' уже существует!")
                print(f"  [ПОДСКАЗКА] Используйте другое название или удалите старую.")
                logger.warning(f"Попытка создать дубликат: {name}")
                name_exists = True
                break

        if name_exists:
            continue

        # Проверка на допустимые символы (только буквы, цифры, пробелы)
        if not all(c.isalnum() or c in ' _-@.' for c in name):
            print("  [ОШИБКА] Название содержит недопустимые символы!")
            print("  [ПОДСКАЗКА] Используйте только буквы, цифры, пробелы, дефисы.")
            continue

        # Название прошло все проверки
        print(f"  [OK] Название: {name}")
        logger.info(f"Название принято: {name}")
        break

    # ==========================================
    # ЭТАП 2: ЛОГИН ИЛИ EMAIL
    # ==========================================
    while True:
        login = input("  Логин или email: ").strip()

        # Проверка на пустой логин
        if not login:
            print("  [ОШИБКА] Логин не может быть пустым!")
            print("  [ПОДСКАЗКА] Введите email (user@mail.com) или логин (@username)")
            logger.warning("Попытка создания записи с пустым логином")
            continue

        # Проверка на слишком короткий логин
        if len(login) < 3:
            print("  [ОШИБКА] Логин слишком короткий (минимум 3 символа)!")
            continue

        # Определяем тип: email или логин
        is_email = '@' in login and '.' in login
        is_login = login.startswith('@') or login.isalnum()

        if is_email:
            # Проверка email
            parts = login.split('@')
            if len(parts) != 2 or not parts[0] or not parts[1]:
                print("  [ОШИБКА] Неверный формат email!")
                print("  [ПОДСКАЗКА] Пример: user@gmail.com")
                logger.warning(f"Неверный формат email: {login}")
                continue

            if '.' not in parts[1]:
                print("  [ОШИБКА] Неверный формат email!")
                print("  [ПОДСКАЗКА] Должна быть точка в домене: user@mail.com")
                continue

            print(f"  [OK] Email: {login}")

        elif is_login:
            # Проверка логина
            if login.startswith('@'):
                # Убираем @ для проверки
                login_clean = login[1:]
                if not login_clean or len(login_clean) < 2:
                    print("  [ОШИБКА] Логин после @ слишком короткий!")
                    print("  [ПОДСКАЗКА] Пример: @username")
                    continue
            else:
                login_clean = login

            print(f"  [OK] Логин: {login}")

        else:
            print("  [ОШИБКА] Неверный формат!")
            print("  [ПОДСКАЗКА] Введите:")
            print("    - Email: user@gmail.com")
            print("    - Логин: @username или username")
            logger.warning(f"Неверный формат логина: {login}")
            continue

        logger.info(f"Логин принят: {login}")
        break

    # ==========================================
    # ЭТАП 3: ПАРОЛЬ
    # ==========================================
    while True:
        print("\n  Как создать пароль?")
        print("  1. Сгенерировать автоматически (БЕЗОПАСНО)")
        print("  2. Ввести свой пароль (с проверкой)")

        choice = input("  Ваш выбор (1/2): ").strip()

        if choice == "1":
            # Генерация
            print("\n  Настройки генерации:")
            length_input = input("  Длина (по умолчанию 16): ").strip()
            length = int(length_input) if length_input.isdigit() and int(length_input) >= 8 else 16

            exclude_similar = input("  Исключить похожие 0/O,l/I? (да/нет, по умолчанию да): ").strip().lower()
            exclude_similar = exclude_similar != "нет"

            use_special = input("  Спецсимволы !@#$? (да/нет, по умолчанию да): ").strip().lower()
            use_special = use_special != "нет"

            password = generator.generate(length=length, exclude_similar=exclude_similar, use_special=use_special)
            print(f"\n  [OK] Сгенерированный пароль: {password}")

            # Проверка надёжности
            strength = generator.check_password_strength(password)
            print(f"  [ОЦЕНКА] {strength['level']}")

            # Подтверждение
            confirm = input("  Использовать этот пароль? (да/нет): ").strip().lower()
            if confirm == "да":
                logger.info(f"Пароль сгенерирован для {name}")
                break
            else:
                print("  Генерирую заново...")
                continue

        elif choice == "2":
            # Ручной ввод
            print("\n  ТРЕБОВАНИЯ К ПАРОЛЮ:")
            print("  - Минимум 8 символов")
            print("  - Хотя бы 1 буква (a-z, A-Z)")
            print("  - Хотя бы 1 цифра (0-9)")
            print("  - Хотя бы 1 спецсимвол (!@#$%^&*)")
            print("  - ЗАПРЕЩЕНЫ: 0, O, o, l, I, i, 1, |")
            print()

            password = input("  Введите пароль: ").strip()

            # Проверка на пустой пароль
            if not password:
                print("  [ОШИБКА] Пароль не может быть пустым!")
                logger.warning("Попытка создания записи с пустым паролем")
                continue

            # Проверка длины
            if len(password) < 8:
                print("  [ОШИБКА] Пароль слишком короткий (минимум 8 символов)!")
                print(f"  [ПОДСКАЗКА] Сейчас: {len(password)} символов, нужно: 8+")
                continue

            # Проверка наличия буквы
            if not any(c.isalpha() for c in password):
                print("  [ОШИБКА] Пароль должен содержать хотя бы 1 букву!")
                print("  [ПОДСКАЗКА] Добавьте буквы: a-z или A-Z")
                continue

            # Проверка наличия цифры
            if not any(c.isdigit() for c in password):
                print("  [ОШИБКА] Пароль должен содержать хотя бы 1 цифру!")
                print("  [ПОДСКАЗКА] Добавьте цифры: 0-9")
                continue

            # Проверка наличия спецсимвола
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                print("  [ОШИБКА] Пароль должен содержать хотя бы 1 спецсимвол!")
                print("  [ПОДСКАЗКА] Добавьте: !@#$%^&*")
                continue

            # ПРОВЕРКА ПОХОЖИХ СИМВОЛОВ
            found_similar = check_similar_chars(password)
            if found_similar:
                print("\n  [ОШИБКА] Обнаружены запрещённые похожие символы:")
                for s in found_similar:
                    print(f"    - {s}")
                print()
                print("  [ПРИЧИНА] Эти символы легко перепутать при вводе.")
                print()
                print("  [РЕШЕНИЕ] Замените:")
                print("    0 -> 2-9 | O -> A,B,C | l -> k,m,n | I -> H,J,K | 1 -> 2-9")
                logger.warning(f"Пароль содержит похожие символы: {password}")
                continue

            # Пароль прошёл все проверки
            strength = generator.check_password_strength(password)
            print(f"\n  [OK] Пароль принят!")
            print(f"  [ОЦЕНКА] {strength['level']} ({strength['score']}/{strength['max_score']})")

            if strength['feedback']:
                print("  [РЕКОМЕНДАЦИИ]:")
                for tip in strength['feedback']:
                    print(f"    - {tip}")

            logger.info(f"Ручной пароль принят для {name}")
            break

        else:
            print("  [ОШИБКА] Выберите 1 или 2!")

    # ==========================================
    # ЭТАП 4: ПОДТВЕРЖДЕНИЕ СОХРАНЕНИЯ
    # ==========================================
    print("\n" + "-" * 50)
    print("  ИТОГ:")
    print(f"    Сервис: {name}")
    print(f"    Логин: {login}")
    print(f"    Пароль: {'*' * len(password)}")
    print("-" * 50)

    while True:
        confirm = input("  Сохранить? (да/нет): ").strip().lower()
        if confirm == "да":
            success = store.add_record(name, login, password)
            if success:
                print(f"\n  [УСПЕХ] Запись '{name}' сохранена!")
                logger.info(f"Создана запись: {name}")
            else:
                print("\n  [ОШИБКА] Не удалось сохранить!")
                logger.error(f"Ошибка сохранения: {name}")
            return
        elif confirm == "нет":
            print("  [ОТМЕНА] Запись не сохранена.")
            return
        else:
            print("  [ОШИБКА] Введите 'да' или 'нет'!")


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
