# -*- coding: utf-8 -*-
"""
==============================================
 ГЛАВНЫЙ ФАЙЛ ПРИЛОЖЕНИЯ
 Менеджер паролей с генерацией паролей
==============================================

 Этот файл является точкой входа в приложение.
 Он запускает главное меню и управляет работой программы.

 Автор: N-888
 Версия: 1.0
 Дата: 2026
"""

# ==========================================
# ИМПОРТ НЕОБХОДИХ БИБЛИОТЕК
# ==========================================

# Импортируем модуль os для работы с файловой системой
# (проверка существования папок и файлов)
import os

# Импортируем модуль json для чтения и записи JSON-файлов
# (хранилище паролей будет в формате JSON)
import json

# Импортируем модуль logging для ведения журнала событий
# (запись действий пользователя и ошибок в файл)
import logging

# Импортируем модуль sys для работы с системными функциями
# (корректное завершение программы)
import sys

# Импортируем модуль io для работы с кодировкой
import io

# Настраиваем кодировку для Windows (чтобы работали эмодзи)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Импортируем наш модуль генератора паролей
# (создаёт безопасные пароли)
from password_generator import PasswordGenerator

# Импортируем наш модуль хранилища паролей
# (сохраняет и загружает пароли из файла)
from password_store import PasswordStore


# ==========================================
# НАСТРОЙКА ЛОГИРОВАНИЯ
# ==========================================

# Создаём папку для логов, если её нет
# Логи — это записи о том, что происходило в программе
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Настраиваем логирование в файл
# Уровень INFO — записываем основные действия
# Формат: дата, время, уровень, сообщение
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Создаём логгер — это объект для записи сообщений
logger = logging.getLogger(__name__)


# ==========================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==========================================

def show_main_menu():
    """
    Показать главное меню приложения.

    Эта функция выводит на экран список доступных действий.
    Пользователь выбирает номер действия для его выполнения.
    """
    print("\n" + "=" * 50)
    print("  🔐 МЕНЕДЖЕР ПАРОЛЕЙ С ГЕНЕРАТОРОМ")
    print("=" * 50)
    print("  1. 📋 Показать все записи")
    print("  2. ➕ Добавить новую запись")
    print("  3. 🔍 Найти запись")
    print("  4. 🗑️  Удалить запись")
    print("  5. 🔑 Сгенерировать пароль")
    print("  6. 📊 Статистика")
    print("  7. ❌ Выход")
    print("=" * 50)


# ==========================================
# ФУНКЦИЯ ПОКАЗА ВСЕХ ЗАПИСЕЙ
# ==========================================

def show_all_records(store):
    """
    Показать все сохранённые записи паролей.

    Аргументы:
        store — объект хранилища паролей

    Эта функция выводит список всех записей с названиями.
    """
    print("\n" + "-" * 50)
    print("  📋 ВСЕ ЗАПИСИ:")
    print("-" * 50)

    # Получаем все записи из хранилища
    records = store.get_all_records()

    # Если записей нет — сообщаем об этом
    if not records:
        print("  📭 Записей пока нет.")
        print("  Добавьте первую запись (пункт 2 в меню)")
        return

    # Перебираем все записи и показываем каждую
    for i, record in enumerate(records, 1):
        # Выводим номер, название и логин
        print(f"  {i}. {record['name']}")
        print(f"     👤 Логин: {record['login']}")
        print(f"     🔑 Пароль: {'*' * len(record['password'])}")
        print()

    print("-" * 50)
    print(f"  📊 Всего записей: {len(records)}")
    print("-" * 50)


# ==========================================
# ФУНКЦИЯ ДОБАВЛЕНИЯ ЗАПИСИ
# ==========================================

def add_new_record(store, generator):
    """
    Добавить новую запись в хранилище.

    Аргументы:
        store — объект хранилища паролей
        generator — объект генератора паролей

    Эта функция запрашивает у пользователя данные
    и сохраняет новую запись.
    """
    print("\n" + "-" * 50)
    print("  ➕ ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ:")
    print("-" * 50)

    try:
        # Запрашиваем название сервиса (например, Gmail, Telegram)
        name = input("  📝 Название сервиса: ").strip()

        # Проверяем, что пользователь ввёл название
        if not name:
            print("  ❌ Ошибка: название не может быть пустым!")
            return

        # Запрашиваем логин или email
        login = input("  👤 Логин или email: ").strip()

        # Проверяем, что логин введён
        if not login:
            print("  ❌ Ошибка: логин не может быть пустым!")
            return

        # Спрашиваем, сгенерировать пароль или ввести свой
        print("\n  🔑 Как создать пароль?")
        print("  1. Сгенерировать автоматически")
        print("  2. Ввести свой пароль")

        choice = input("  Ваш выбор (1/2): ").strip()

        if choice == "1":
            # Генерируем пароль автоматически
            print("\n  ⚙️  Настройки генерации:")
            print("  (Нажмите Enter для значений по умолчанию)")

            # Запрашиваем длину пароля
            length_input = input("  📏 Длина пароля (по умолчанию 16): ").strip()
            length = int(length_input) if length_input.isdigit() else 16

            # Спрашиваем, исключать ли похожие символы
            exclude_similar = input("  🚫 Исключить похожие символы (0/O, l/I)? (да/нет, по умолчанию да): ").strip().lower()
            exclude_similar = exclude_similar != "нет"

            # Спрашиваем, использовать ли спецсимволы
            use_special = input("  ✨ Использовать спецсимволы (!@#$%...)? (да/нет, по умолчанию да): ").strip().lower()
            use_special = use_special != "нет"

            # Генерируем пароль с указанными параметрами
            password = generator.generate(
                length=length,
                exclude_similar=exclude_similar,
                use_special=use_special
            )

            # Показываем сгенерированный пароль
            print(f"\n  ✅ Сгенерированный пароль: {password}")

        elif choice == "2":
            # Пользователь вводит свой пароль
            password = input("  🔑 Введите пароль: ").strip()

            if not password:
                print("  ❌ Ошибка: пароль не может быть пустым!")
                return

            # Проверяем наличие похожих символов
            similar_chars = {'0': 'ноль/O', 'O': 'О/ноль', 'l': 'строчная Л/I', 'I': 'I/строчная Л', '1': 'единица/l'}
            found_similar = [f"'{c}' ({similar_chars[c]})" for c in password if c in similar_chars]

            if found_similar:
                print(f"\n  ⚠️  ВНИМАНИЕ! В пароле обнаружены похожие символы:")
                for s in found_similar:
                    print(f"     • {s}")
                print("  💡 Это может затруднить ввод пароля вручную.")
                print("  💡 Рекомендуется заменить их на более чёткие символы.")

                confirm = input("\n  Сохранить пароль с похожими символами? (да/нет): ").strip().lower()
                if confirm != "да":
                    print("  🔄 Введите пароль заново.")
                    return
        else:
            print("  ❌ Неверный выбор!")
            return

        # Сохраняем запись в хранилище
        success = store.add_record(name, login, password)

        if success:
            print(f"\n  ✅ Запись «{name}» успешно добавлена!")
            logger.info(f"Добавлена новая запись: {name}")

            # Проверяем надёжность пароля
            strength = generator.check_password_strength(password)
            print(f"\n  📊 Оценка пароля: {strength['level']} ({strength['score']}/{strength['max_score']})")

            # Если есть замечания — показываем их
            if strength['feedback']:
                print("  ⚠️  Рекомендации:")
                for tip in strength['feedback']:
                    print(f"     • {tip}")
        else:
            print("\n  ❌ Ошибка при сохранении записи!")

    except ValueError as e:
        # Ошибка ввода числа
        print(f"  ❌ Ошибка ввода: {e}")
        logger.error(f"Ошибка ввода: {e}")
    except Exception as e:
        # Любая другая ошибка
        print(f"  ❌ Непредвиденная ошибка: {e}")
        logger.error(f"Непредвиденная ошибка: {e}")


# ==========================================
# ФУНКЦИЯ ПОИСКА ЗАПИСИ
# ==========================================

def search_record(store):
    """
    Найти запись по названию.

    Аргументы:
        store — объект хранилища паролей

    Эта функция ищет запись по части названия.
    """
    print("\n" + "-" * 50)
    print("  🔍 ПОИСК ЗАПИСИ:")
    print("-" * 50)

    try:
        # Запрашиваем поисковый запрос
        query = input("  🔎 Введите название или часть названия: ").strip()

        if not query:
            print("  ❌ Ошибка: введите запрос для поиска!")
            return

        # Ищем записи по запросу
        results = store.search_records(query)

        if not results:
            print(f"  📭 Записи «{query}» не найдены.")
            return

        # Показываем найденные записи
        print(f"\n  ✅ Найдено записей: {len(results)}")
        print("-" * 50)

        for record in results:
            print(f"  📌 {record['name']}")
            print(f"     👤 Логин: {record['login']}")
            print(f"     🔑 Пароль: {record['password']}")
            print()

    except Exception as e:
        print(f"  ❌ Ошибка поиска: {e}")
        logger.error(f"Ошибка поиска: {e}")


# ==========================================
# ФУНКЦИЯ УДАЛЕНИЯ ЗАПИСИ
# ==========================================

def delete_record(store):
    """
    Удалить запись по номеру.

    Аргументы:
        store — объект хранилища паролей

    Эта функция удаляет запись после подтверждения.
    """
    print("\n" + "-" * 50)
    print("  🗑️  УДАЛЕНИЕ ЗАПИСИ:")
    print("-" * 50)

    try:
        # Показываем все записи
        records = store.get_all_records()

        if not records:
            print("  📭 Записей для удаления нет.")
            return

        # Показываем список с номерами
        for i, record in enumerate(records, 1):
            print(f"  {i}. {record['name']}")

        # Запрашиваем номер записи для удаления
        num_input = input("\n  🔢 Введите номер записи для удаления: ").strip()

        if not num_input.isdigit():
            print("  ❌ Ошибка: введите число!")
            return

        num = int(num_input) - 1

        # Проверяем, что номер правильный
        if num < 0 or num >= len(records):
            print("  ❌ Ошибка: неверный номер записи!")
            return

        # Получаем запись для удаления
        record = records[num]

        # Спрашиваем подтверждение
        confirm = input(f"  ⚠️  Удалить «{record['name']}»? (да/нет): ").strip().lower()

        if confirm == "да":
            success = store.delete_record(record['name'])
            if success:
                print(f"\n  ✅ Запись «{record['name']}» удалена!")
                logger.info(f"Удалена запись: {record['name']}")
            else:
                print("\n  ❌ Ошибка при удалении!")
        else:
            print("  🔄 Удаление отменено.")

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        logger.error(f"Ошибка удаления: {e}")


# ==========================================
# ФУНКЦИЯ ГЕНЕРАЦИИ ПАРОЛЯ
# ==========================================

def generate_password_menu(generator):
    """
    Отдельное меню генерации пароля.

    Аргументы:
        generator — объект генератора паролей

    Эта функция позволяет сгенерировать пароль
    без сохранения в хранилище.
    """
    print("\n" + "-" * 50)
    print("  🔑 ГЕНЕРАТОР ПАРОЛЕЙ:")
    print("-" * 50)

    try:
        # Запрашиваем настройки генерации
        print("  ⚙️  Настройки генерации:")
        print("  (Нажмите Enter для значений по умолчанию)")

        # Длина пароля
        length_input = input("  📏 Длина пароля (по умолчанию 16): ").strip()
        length = int(length_input) if length_input.isdigit() else 16

        # Исключение похожих символов
        exclude_similar = input("  🚫 Исключить похожие символы (0/O, l/I)? (да/нет, по умолчанию да): ").strip().lower()
        exclude_similar = exclude_similar != "нет"

        # Использование спецсимволов
        use_special = input("  ✨ Использовать спецсимволы (!@#$%...)? (да/нет, по умолчанию да): ").strip().lower()
        use_special = use_special != "нет"

        # Количество паролей
        count_input = input("  🔢 Сколько паролей сгенерировать (по умолчанию 1): ").strip()
        count = int(count_input) if count_input.isdigit() else 1

        print("\n" + "=" * 50)
        print("  🎲 СГЕНЕРИРОВАННЫЕ ПАРОЛИ:")
        print("=" * 50)

        # Генерируем указанное количество паролей
        for i in range(count):
            password = generator.generate(
                length=length,
                exclude_similar=exclude_similar,
                use_special=use_special
            )
            print(f"  {i + 1}. {password}")

        print("=" * 50)
        logger.info(f"Сгенерировано {count} паролей")

    except ValueError as e:
        print(f"  ❌ Ошибка ввода: {e}")
    except Exception as e:
        print(f"  ❌ Ошибка генерации: {e}")
        logger.error(f"Ошибка генерации: {e}")


# ==========================================
# ФУНКЦИЯ СТАТИСТИКИ
# ==========================================

def show_statistics(store):
    """
    Показать статистику по хранилищу.

    Аргументы:
        store — объект хранилища паролей

    Эта функция показывает общую информацию о записях.
    """
    print("\n" + "-" * 50)
    print("  📊 СТАТИСТИКА:")
    print("-" * 50)

    try:
        # Получаем статистику из хранилища
        stats = store.get_statistics()

        # Показываем статистику
        print(f"  📋 Всего записей: {stats['total_records']}")
        print(f"  📁 Файл хранилища: {stats['file_size']} байт")
        print(f"  📅 Последнее обновление: {stats['last_modified']}")
        print("-" * 50)

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        logger.error(f"Ошибка статистики: {e}")


# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================

def main():
    """
    Главная функция приложения.

    Эта функция:
    1. Инициализирует компоненты
    2. Показывает приветствие
    3. Запускает главный цикл меню
    4. Обрабатывает выбор пользователя
    5. Корректно завершает работу
    """
    # Выводим приветствие
    print("\n" + "🌟" * 25)
    print("  Добро пожаловать в Менеджер паролей!")
    print("  Безопасное хранение и генерация паролей")
    print("🌟" * 25)

    try:
        # Создаём объект генератора паролей
        generator = PasswordGenerator()
        logger.info("Генератор паролей инициализирован")

        # Создаём объект хранилища паролей
        store = PasswordStore()
        logger.info("Хранилище паролей инициализировано")

        # Добавляем тестовые записи, если хранилище пустое
        if store.get_statistics()['total_records'] == 0:
            print("\n  📝 Добавляем тестовые записи...")
            store.add_record("Gmail", "user@gmail.com", "MySecurePass123!")
            store.add_record("Telegram", "@username", "TelegramPass456!")
            print("  ✅ Добавлены 2 тестовые записи: Gmail и Telegram")
            logger.info("Добавлены тестовые записи")

        # Главный цикл приложения
        while True:
            # Показываем меню
            show_main_menu()

            # Запрашиваем выбор пользователя
            choice = input("\n  🔢 Ваш выбор (1-7): ").strip()

            # Обрабатываем выбор
            if choice == "1":
                # Показать все записи
                show_all_records(store)

            elif choice == "2":
                # Добавить новую запись
                add_new_record(store, generator)

            elif choice == "3":
                # Найти запись
                search_record(store)

            elif choice == "4":
                # Удалить запись
                delete_record(store)

            elif choice == "5":
                # Сгенерировать пароль
                generate_password_menu(generator)

            elif choice == "6":
                # Показать статистику
                show_statistics(store)

            elif choice == "7":
                # Выход из программы
                print("\n  👋 До свидания! Ваши пароли в безопасности.")
                logger.info("Пользователь завершил работу")
                break

            else:
                # Неверный выбор
                print("\n  ❌ Неверный выбор! Введите число от 1 до 7.")

    except KeyboardInterrupt:
        # Пользователь нажал Ctrl+C — корректно выходим
        print("\n\n  👋 Программа завершена.")
        logger.info("Программа завершена через Ctrl+C")

    except Exception as e:
        # Непредвиденная ошибка
        print(f"\n  💥 Критическая ошибка: {e}")
        logger.critical(f"Критическая ошибка: {e}")
        sys.exit(1)


# ==========================================
# ЗАПУСК ПРОГРАММЫ
# ==========================================

# Эта команда запускает главную функцию
# только если файл запущен напрямую (не импортирован)
if __name__ == "__main__":
    main()
