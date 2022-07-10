class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration_h = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration_h:.3f} ч.;'
            f' Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч;'
            f' Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    COEFF_SPENT_CALOEIES_1: float
    COEFF_SPENT_CALOEIES_2: float
    MIN_PER_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration_h,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_SPENT_CALOEIES_1: float = 18
    COEFF_SPENT_CALOEIES_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_SPENT_CALOEIES_1
                * self.get_mean_speed()
                - self.COEFF_SPENT_CALOEIES_2)
                * self.weight_kg
                / self.M_IN_KM
                * self.duration_h * self.MIN_PER_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_SPENT_CALOEIES_1: float = 0.035
    COEFF_SPENT_CALOEIES_2: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height
        self.duration_m = self.duration_h * self.MIN_PER_HOUR

    def get_spent_calories(self) -> float:

        return (
            (self.COEFF_SPENT_CALOEIES_1
             * self.weight_kg
             + ((self.get_mean_speed())**2 // self.height_cm)
             * self.COEFF_SPENT_CALOEIES_2
             * self.weight_kg) * self.duration_m
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SPENT_CALOEIES_1: float = 1.1
    COEFF_SPENT_CALOEIES_2: float = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration_h
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.COEFF_SPENT_CALOEIES_1)
            * self.COEFF_SPENT_CALOEIES_2 * self.weight_kg
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    types_of_training: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in types_of_training:
        return types_of_training[workout_type](*data)

    raise ValueError(
        f'Тип тренировки {workout_type} не найден'
    )


def main(training: Training) -> None:
    """Главная функция."""
    info_message = training.show_training_info()
    info_string = info_message.get_message()
    print(info_string)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
