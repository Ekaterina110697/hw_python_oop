from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    # Конструктор класса. Здесь задаются основные параметры сообщения.
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: int,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    # Метод для получения отформатированного сообщения о тренировке.
    def get_message(self) -> str:
        result = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )
        return result


class Training:
    """Базовый класс тренировки."""

    # Основные константы для всех тренировок.
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    # Конструктор базового класса.
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # Расчет дистанции тренировки.
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    # Расчет средней скорости.
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    # Создание объекта InfoMessage для текущей тренировки.
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    # Константы для расчета калорий в беге.
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    # Переопределенный метод для расчета затраченных калорий в беге.
    def get_spent_calories(self) -> float:
        return (
            ((
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()) + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )

# --- Тренировка: спортивная ходьба ---


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Константы для расчета калорий в спортивной ходьбе.
    WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER: float = 0.029
    M_IN_SM: int = 100
    KM_H_IN_M_S: float = 0.278

    # Конструктор с дополнительным параметром для спортивной ходьбы.
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> float:
        super().__init__(action, duration, weight)
        self.height = height

    # Переопределенный метод для расчета калорий в спортивной ходьбе.

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (
                self.WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KM_H_IN_M_S) ** 2
                    / self.height * self.M_IN_SM)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    # Константы и параметры для тренировки плавания.
    LEN_STEP: float = 1.38
    SPEED_CORRECT_FACTOR_1: float = 1.1  # сдвиг для скорости
    SPEED_CORRECTION_FACTOR_2: int = 2  # множитель для скорости

    # Конструктор с дополнительными параметрами для плавания.
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool,
        count_pool: int,
    ) -> float:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # Переопределенный метод для расчета средней скорости в плавании.
    def get_mean_speed(self):
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    # Переопределенный метод для расчета калорий в плавании.
    def get_spent_calories(self):
        return (
            ((
                self.get_mean_speed()
                + self.SPEED_CORRECT_FACTOR_1) * self.SPEED_CORRECTION_FACTOR_2
             * self.weight * self.duration)
        )


# --- Чтение данных о тренировке ---

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Словарь типов тренировок и соответствующих классов.
    workouts: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }

    # Если входной тип тренировки отсутствует в словаре, возникает ошибка.
    if workout_type not in workouts:
        raise ValueError("Нет такого типа тренироовки")

    # Возвращает экземпляр класса тренировки с данными из пакета.
    return workouts.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    # Выводит информацию о тренировке в консоль.
    print(training.show_training_info().get_message())


# Запуск кода, если он не импортирован как модуль.
if __name__ == "__main__":
    # Примеры тренировок для тестов.
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    # Для каждого пакета данных выводит информацию о тренировке.
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
