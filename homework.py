class InfoMessage:
    """Информационное сообщение о тренировке."""
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

    def get_message(self) -> str:
        """Отформатированное сообщение о тренировке."""
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    # Основные константы для всех тренировок.
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется определить get_spent_calories()")

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
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            ((
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()) + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Константы для расчета калорий в спортивной ходьбе.
    WEIGHT_MULTIPLIER_1: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029
    M_IN_SM: int = 100
    KM_H_IN_M_S: float = 0.278

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float,
    ) -> float:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (
                self.WEIGHT_MULTIPLIER_1 * self.weight
                + (
                    (self.get_mean_speed() * self.KM_H_IN_M_S) ** 2
                    / self.height * self.M_IN_SM)
                * self.WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    # Константы и параметры для тренировки плавания.
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

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

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (
            ((
                self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.weight * self.duration)
        )


WORKOUTS: dict[str, type[Training]] = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUTS:
        raise ValueError(f"{workout_type} нет такого типа тренировки")

    return WORKOUTS.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
