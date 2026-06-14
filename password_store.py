# -*- coding: utf-8 -*-
"""
==============================================
 МОДУЛЬ ХРАНИЛИЩА ПАРОЛЕЙ
==============================================

 Этот модуль сохраняет и загружает пароли.
 Пароли хранятся в JSON-файле.

 Автор: N-888
 Версия: 1.0
 Дата: 2026
"""

# ==========================================
# ИМПОРТ НЕОБХОДИМЫХ БИБЛИОТЕК
# ==========================================

# Импортируем модуль json для работы с JSON-файлами
import json

# Импортируем модуль os для работы с файловой системой
import os

# Импортируем модуль logging для записи ошибок
import logging

# Импортируем модуль hashlib для хеширования паролей
import hashlib

# Импортируем модуль datetime для работы с датой и временем
from datetime import datetime

# Создаём логгер для этого модуля
logger = logging.getLogger(__name__)


# ==========================================
# КЛАСС ХРАНИЛИЩА ПАРОЛЕЙ
# ==========================================

class PasswordStore:
    """
    Класс для хранения и управления парами логин/пароль.

    Этот класс:
    - Сохраняет пароли в JSON-файл
    - Загружает пароли из файла
    - Позволяет добавлять, удалять, искать записи

    Пример использования:
        store = PasswordStore()
        store.add_record("Gmail", "user@gmail.com", "mypassword")
        records = store.get_all_records()
    """

    # ==========================================
    # ИНИЦИАЛИЗАЦИЯ
    # ==========================================

    def __init__(self, filename="passwords.json"):
        """
        Инициализация хранилища паролей.

        Аргументы:
            filename (str): Имя файла для хранения паролей
                           (по умолчанию "passwords.json")
        """
        # Сохраняем имя файла
        self.filename = filename

        # Загружаем данные из файла (если он существует)
        self.records = self._load_from_file()

        # Сообщаем о создании хранилища
        logger.info(f"Хранилище паролей создано: {filename}")
        print(f"  ✅ Хранилище готово: {filename}")

    # ==========================================
    # ЗАГРУЗКА ДАННЫХ ИЗ ФАЙЛА
    # ==========================================

    def _load_from_file(self):
        """
        Загрузить данные из JSON-файла.

        Эта функция читает файл и возвращает список записей.
        Если файла нет — создаёт пустой список.

        Возвращает:
            list: Список записей паролей
        """
        try:
            # Проверяем, существует ли файл
            if os.path.exists(self.filename):
                # Открываем файл для чтения
                with open(self.filename, 'r', encoding='utf-8') as f:
                    # Читаем JSON-данные
                    data = json.load(f)

                # Сообщаем о загрузке
                logger.info(f"Загружено {len(data)} записей из {self.filename}")
                return data
            else:
                # Файла нет — возвращаем пустой список
                logger.info(f"Файл {self.filename} не найден, создаём новый")
                return []

        except json.JSONDecodeError as e:
            # Ошибка формата JSON
            logger.error(f"Ошибка формата JSON: {e}")
            print(f"  ⚠️  Ошибка чтения файла: {e}")
            return []

        except Exception as e:
            # Любая другая ошибка
            logger.error(f"Ошибка загрузки файла: {e}")
            print(f"  ⚠️  Ошибка: {e}")
            return []

    # ==========================================
    # СОХРАНЕНИЕ ДАННЫХ В ФАЙЛ
    # ==========================================

    def _save_to_file(self):
        """
        Сохранить данные в JSON-файл.

        Эта функция записывает текущий список записей в файл.
        """
        try:
            # Открываем файл для записи
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Записываем JSON-данные с отступами для читаемости
                json.dump(self.records, f, ensure_ascii=False, indent=4)

            # Сообщаем об успешном сохранении
            logger.info(f"Сохранено {len(self.records)} записей в {self.filename}")
            return True

        except Exception as e:
            # Ошибка сохранения
            logger.error(f"Ошибка сохранения файла: {e}")
            print(f"  ❌ Ошибка сохранения: {e}")
            return False

    # ==========================================
    # ДОБАВЛЕНИЕ ЗАПИСИ
    # ==========================================

    def add_record(self, name, login, password):
        """
        Добавить новую запись в хранилище.

        Аргументы:
            name (str): Название сервиса (Gmail, Telegram)
            login (str): Логин или email
            password (str): Пароль

        Возвращает:
            bool: True если успешно, False если ошибка

        Пример:
            store = PasswordStore()
            store.add_record("Gmail", "user@gmail.com", "mypassword123")
        """
        try:
            # Проверяем, что все поля заполнены
            if not name or not login or not password:
                logger.error("Попытка добавить запись с пустыми полями")
                return False

            # Проверяем, нет ли уже такой записи
            for record in self.records:
                if record['name'].lower() == name.lower():
                    logger.warning(f"Запись «{name}» уже существует")
                    print(f"  ⚠️  Запись «{name}» уже существует!")
                    return False

            # Создаём новую запись
            new_record = {
                "name": name,           # Название сервиса
                "login": login,         # Логин или email
                "password": password,   # Пароль
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Добавляем запись в список
            self.records.append(new_record)

            # Сохраняем в файл
            success = self._save_to_file()

            if success:
                logger.info(f"Добавлена запись: {name}")
                return True
            else:
                # Если не удалось сохранить — удаляем из списка
                self.records.pop()
                return False

        except Exception as e:
            logger.error(f"Ошибка добавления записи: {e}")
            return False

    # ==========================================
    # ПОЛУЧЕНИЕ ВСЕХ ЗАПИСЕЙ
    # ==========================================

    def get_all_records(self):
        """
        Получить все записи из хранилища.

        Возвращает:
            list: Список всех записей

        Пример:
            store = PasswordStore()
            records = store.get_all_records()
            for record in records:
                print(record['name'])
        """
        logger.info(f"Запрошены все записи (всего: {len(self.records)})")
        return self.records

    # ==========================================
    # ПОИСК ЗАПИСЕЙ
    # ==========================================

    def search_records(self, query):
        """
        Найти записи по запросу.

        Аргументы:
            query (str): Строка для поиска (название сервиса)

        Возвращает:
            list: Список найденных записей

        Пример:
            store = PasswordStore()
            results = store.search_records("gmail")
        """
        # Ищем записи, где название содержит запрос
        results = [
            record for record in self.records
            if query.lower() in record['name'].lower()
        ]

        logger.info(f"Поиск «{query}»: найдено {len(results)} записей")
        return results

    # ==========================================
    # УДАЛЕНИЕ ЗАПИСИ
    # ==========================================

    def delete_record(self, name):
        """
        Удалить запись по названию.

        Аргументы:
            name (str): Название сервиса для удаления

        Возвращает:
            bool: True если успешно, False если не найдено

        Пример:
            store = PasswordStore()
            store.delete_record("Gmail")
        """
        try:
            # Ищем запись с таким названием
            for i, record in enumerate(self.records):
                if record['name'].lower() == name.lower():
                    # Удаляем запись
                    deleted = self.records.pop(i)

                    # Сохраняем изменения
                    success = self._save_to_file()

                    if success:
                        logger.info(f"Удалена запись: {name}")
                        return True
                    else:
                        # Если не удалось сохранить — возвращаем запись
                        self.records.insert(i, deleted)
                        return False

            # Запись не найдена
            logger.warning(f"Запись «{name}» не найдена для удаления")
            return False

        except Exception as e:
            logger.error(f"Ошибка удаления записи: {e}")
            return False

    # ==========================================
    # ОБНОВЛЕНИЕ ЗАПИСИ
    # ==========================================

    def update_record(self, name, new_login=None, new_password=None):
        """
        Обновить запись в хранилище.

        Аргументы:
            name (str): Название сервиса для обновления
            new_login (str): Новый логин (если None — не менять)
            new_password (str): Новый пароль (если None — не менять)

        Возвращает:
            bool: True если успешно, False если не найдено

        Пример:
            store = PasswordStore()
            store.update_record("Gmail", new_password="newpass123")
        """
        try:
            # Ищем запись
            for record in self.records:
                if record['name'].lower() == name.lower():
                    # Обновляем поля, если указаны
                    if new_login is not None:
                        record['login'] = new_login
                    if new_password is not None:
                        record['password'] = new_password

                    # Обновляем время изменения
                    record['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Сохраняем изменения
                    success = self._save_to_file()

                    if success:
                        logger.info(f"Обновлена запись: {name}")
                        return True
                    return False

            logger.warning(f"Запись «{name}» не найдена для обновления")
            return False

        except Exception as e:
            logger.error(f"Ошибка обновления записи: {e}")
            return False

    # ==========================================
    # СТАТИСТИКА
    # ==========================================

    def get_statistics(self):
        """
        Получить статистику по хранилищу.

        Возвращает:
            dict: Словарь со статистикой

        Пример:
            store = PasswordStore()
            stats = store.get_statistics()
            print(stats['total_records'])
        """
        try:
            # Подсчитываем количество записей
            total = len(self.records)

            # Получаем размер файла
            if os.path.exists(self.filename):
                file_size = os.path.getsize(self.filename)
            else:
                file_size = 0

            # Получаем время последнего изменения файла
            if os.path.exists(self.filename):
                mtime = os.path.getmtime(self.filename)
                last_modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            else:
                last_modified = "Файл не найден"

            return {
                "total_records": total,
                "file_size": file_size,
                "last_modified": last_modified,
                "filename": self.filename
            }

        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {
                "total_records": 0,
                "file_size": 0,
                "last_modified": "Ошибка",
                "filename": self.filename
            }

    # ==========================================
    # ЭКСПОРТ ДАННЫХ
    # ==========================================

    def export_to_text(self, filename="export.txt"):
        """
        Экспортировать записи в текстовый файл.

        Аргументы:
            filename (str): Имя файла для экспорта

        Возвращает:
            bool: True если успешно

        Пример:
            store = PasswordStore()
            store.export_to_text("my_passwords.txt")
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ЭКСПОРТ ПАРОЛЕЙ\n")
                f.write("=" * 50 + "\n\n")

                for record in self.records:
                    f.write(f"Название: {record['name']}\n")
                    f.write(f"Логин: {record['login']}\n")
                    f.write(f"Пароль: {record['password']}\n")
                    f.write(f"Создано: {record['created_at']}\n")
                    f.write("-" * 50 + "\n\n")

            logger.info(f"Данные экспортированы в {filename}")
            return True

        except Exception as e:
            logger.error(f"Ошибка экспорта: {e}")
            return False
