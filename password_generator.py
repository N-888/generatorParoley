# -*- coding: utf-8 -*-
"""
==============================================
 МОДУЛЬ ГЕНЕРАТОРА ПАРОЛЕЙ
==============================================

 Этот модуль создаёт безопасные пароли.
 Можно настроить:
   - длину пароля
   - исключение похожих символов (0/O, l/I)
   - использование спецсимволов

 Автор: N-888
 Версия: 1.0
 Дата: 2026
"""

# ==========================================
# ИМПОРТ НЕОБХОДИМЫХ БИБЛИОТЕК
# ==========================================

# Импортируем модуль random для случайного выбора символов
import random

# Импортируем модуль string для получения наборов символов
import string

# Импортируем модуль logging для записи ошибок
import logging

# Создаём логгер для этого модуля
logger = logging.getLogger(__name__)


# ==========================================
# КЛАСС ГЕНЕРАТОРА ПАРОЛЕЙ
# ==========================================

class PasswordGenerator:
    """
    Класс для генерации безопасных паролей.

    Этот класс создаёт пароли с различными настройками:
    - Длина пароля
    - Исключение похожих символов
    - Использование спецсимволов

    Пример использования:
        generator = PasswordGenerator()
        password = generator.generate(length=16)
    """

    # ==========================================
    # ОПРЕДЕЛЕНИЕ НАБОРОВ СИМВОЛОВ
    # ==========================================

    # Маленькие буквы: a-z
    LOWERCASE = string.ascii_lowercase  # abcdefghijklmnopqrstuvwxyz

    # Большие буквы: A-Z
    UPPERCASE = string.ascii_uppercase  # ABCDEFGHIJKLMNOPQRSTUVWXYZ

    # Цифры: 0-9
    DIGITS = string.digits  # 0123456789

    # Спецсимволы: !@#$%^&*()_+-=[]{}|;:,.<>?
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # ==========================================
    # ПАРА НОЖНИЦЫ (похожие символы)
    # ==========================================

    # Символы, которые легко перепутать:
    # 0 (ноль) и O (буква О)
    # l (строчная Л) и I (заглавная I)
    # 1 (единица) и l (строчная Л)
    SIMILAR_CHARS = {
        '0': 'O',  # Ноль похож на букву О
        'O': '0',  # Буква О похожа на ноль
        'l': 'I',  # Строчная Л похожа на I
        'I': 'l',  # Заглавная I похожа на строчную Л
        '1': 'l',  # Единица похожа на строчную Л
        'l': '1',  # Строчная Л похожа на единицу
    }

    # ==========================================
    # ИНИЦИАЛИЗАЦИЯ
    # ==========================================

    def __init__(self):
        """
        Инициализация генератора паролей.

        Эта функция вызывается при создании нового объекта.
        Она настраивает генератор для работы.
        """
        # Сообщаем о создании генератора
        logger.info("Генератор паролей создан")
        print("  ✅ Генератор паролей готов к работе")

    # ==========================================
    # ОСНОВНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ
    # ==========================================

    def generate(self, length=16, exclude_similar=True, use_special=True):
        """
        Сгенерировать безопасный пароль.

        Аргументы:
            length (int): Длина пароля (по умолчанию 16)
            exclude_similar (bool): Исключить похожие символы (по умолчанию True)
            use_special (bool): Использовать спецсимволы (по умолчанию True)

        Возвращает:
            str: Сгенерированный пароль

        Пример:
            generator = PasswordGenerator()
            password = generator.generate(length=20, exclude_similar=True)
            print(password)  # Например: "aB3$kL9#mN2@pQ5!"
        """
        try:
            # Проверяем, что длина пароля не меньше 4
            if length < 4:
                length = 4
                logger.warning("Длина пароля увеличена до 4 (минимум)")
                print("  ⚠️  Минимальная длина пароля: 4 символа")

            # ==========================================
            # ФОРМИРУЕМ НАБОР СИМВОЛОВ
            # ==========================================

            # Начинаем с маленьких и больших букв
            chars = self.LOWERCASE + self.UPPERCASE

            # Добавляем цифры
            chars += self.DIGITS

            # Если нужны спецсимволы — добавляем их
            if use_special:
                chars += self.SPECIAL

            # ==========================================
            # ИСКЛЮЧАЕМ ПОХОЖИЕ СИМВОЛЫ
            # ==========================================

            if exclude_similar:
                # Удаляем похожие символы из набора
                # Это делает пароль более читаемым
                for char in self.SIMILAR_CHARS:
                    chars = chars.replace(char, '')

                logger.info("Похожие символы исключены (0/O, l/I)")
                print("  🚫 Похожие символы исключены")

            # Проверяем, что остались символы для генерации
            if not chars:
                logger.error("Нет доступных символов для генерации")
                raise ValueError("Нет доступных символов")

            # ==========================================
            # ГЕНЕРИРУЕМ ПАРОЛЬ
            # ==========================================

            # Создаём список символов пароля
            password_chars = []

            # Гарантируем, что пароль содержит:
            # - хотя бы одну маленькую букву
            password_chars.append(random.choice(self.LOWERCASE))

            # - хотя бы одну большую букву
            password_chars.append(random.choice(self.UPPERCASE))

            # - хотя бы одну цифру
            password_chars.append(random.choice(self.DIGITS))

            # - хотя бы один спецсимвол (если включены)
            if use_special:
                password_chars.append(random.choice(self.SPECIAL))

            # ==========================================
            # ДОПОЛНЯЕМ ДО НУЖНОЙ ДЛИНЫ
            # ==========================================

            # Добавляем оставшиеся символы случайным образом
            while len(password_chars) < length:
                # Выбираем случайный символ из набора
                char = random.choice(chars)
                password_chars.append(char)

            # ==========================================
            # ПЕРЕМЕШИВАЕМ СИМВОЛЫ
            # ==========================================

            # Перемешиваем символы, чтобы гарантии не были в начале
            random.shuffle(password_chars)

            # Собираем пароль из символов
            password = ''.join(password_chars)

            # Записываем в лог
            logger.info(f"Сгенерирован пароль длиной {length} символов")

            # Возвращаем результат
            return password

        except Exception as e:
            # Если произошла ошибка — логируем и пробрасываем
            logger.error(f"Ошибка генерации пароля: {e}")
            raise

    # ==========================================
    # ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
    # ==========================================

    def generate_pin(self, length=4):
        """
        Сгенерировать PIN-код (только цифры).

        Аргументы:
            length (int): Длина PIN-кода (по умолчанию 4)

        Возвращает:
            str: PIN-код

        Пример:
            generator = PasswordGenerator()
            pin = generator.generate_pin()
            print(pin)  # Например: "7392"
        """
        try:
            # Генерируем строку из цифр
            pin = ''.join(random.choice(self.DIGITS) for _ in range(length))
            logger.info(f"Сгенерирован PIN-код длиной {length}")
            return pin
        except Exception as e:
            logger.error(f"Ошибка генерации PIN: {e}")
            raise

    def generate_passphrase(self, word_count=4):
        """
        Сгенерировать пароль-фразу (набор слов).

        Аргументы:
            word_count (int): Количество слов (по умолчанию 4)

        Возвращает:
            str: Пароль-фраза

        Пример:
            generator = PasswordGenerator()
            phrase = generator.generate_passphrase()
            print(phrase)  # Например: "дом кот солнце река"
        """
        try:
            # Простой список слов для фразы
            words = [
                "дом", "кот", "солнце", "река", "лес", "море",
                "небо", "звезда", "луна", "облако", "ветер", "дождь",
                "снег", "огонь", "камень", "дерево", "цветок", "птица",
                "рыба", "волк", "медведь", "лиса", "заяц", "ёж"
            ]

            # Выбираем случайные слова
            selected_words = random.sample(words, word_count)

            # Соединяем слова через дефис
            passphrase = '-'.join(selected_words)

            logger.info(f"Сгенерирована пароль-фраза из {word_count} слов")
            return passphrase

        except Exception as e:
            logger.error(f"Ошибка генерации фразы: {e}")
            raise

    def check_password_strength(self, password):
        """
        Проверить надёжность пароля.

        Аргументы:
            password (str): Пароль для проверки

        Возвращает:
            dict: Словарь с результатами проверки

        Пример:
            generator = PasswordGenerator()
            result = generator.check_password_strength("MyPass123!")
            print(result)
        """
        # Начинаем с нулевого счёта
        score = 0
        feedback = []

        # Проверяем длину
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        else:
            feedback.append("Рекомендуется длина 16+ символов")

        # Проверяем наличие маленьких букв
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Добавьте маленькие буквы")

        # Проверяем наличие больших букв
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Добавьте большие буквы")

        # Проверяем наличие цифр
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Добавьте цифры")

        # Проверяем наличие спецсимволов
        if any(c in self.SPECIAL for c in password):
            score += 1
        else:
            feedback.append("Добавьте спецсимволы (!@#$...)")

        # Проверяем на похожие символы
        has_similar = any(c in self.SIMILAR_CHARS for c in password)
        if has_similar:
            feedback.append("Есть похожие символы (0/O, l/I)")

        # Определяем уровень надёжности
        if score <= 2:
            level = "🔴 Слабый"
        elif score <= 4:
            level = "🟡 Средний"
        elif score <= 5:
            level = "🟢 Хороший"
        else:
            level = "💚 Отличный"

        return {
            "score": score,
            "max_score": 7,
            "level": level,
            "feedback": feedback,
            "length": len(password)
        }
