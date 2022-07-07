from dataclasses import dataclass
from typing import Optional


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:

        info = (
                f'Тип тренировки: {self.training_type};',
                f'Длительность: {self.duration:.3f} ч.;',
                f'Дистанция: {self.distance:.3f} км;',
                f'Ср. скорость: {self.speed:.3f} км/ч;',
                f'Потрачено ккал: {self.calories:.3f}.'
        )

        return ' '.join(info)


@dataclass
class Training:
    """
    Базовый класс тренировки.
    Последовательность принимаемых данных:
    action - Кол-во совершённых действий.Тип - Int
        Дефолтное значение - остутсвует.
    duration - Длительность тренировки. Тип - Float.
        Дефолтное значение - остутсвует.
    variable_data_1 - Переменная, которая, в зависимости от от класса,
        будет принимать значение, уникальное для этого класса.
        Если класс содержит данную переменную - в docstring имеется
        описание данной переменной. Дефолтное значение - none.
    variable_data_2 - Переменная, которая, в зависимости от от класса,
        будет принимать значение, уникальное для этого класса.
        Если класс содержит данную переменную - в docstring имеется
        описание данной переменной. Дефолтное значение - none.
    LEN_STEP - Константа, определяющая длину действия (шага/гребка и т.д.).
        Дефолтное значение - 0.65
    M_IN_KM - Контанта, отображающая количество метров в 1км.
        Дефолтное значение - 1000
    """
    action: int
    duration: float  # Продолжительность тренировки (передается всегда в часах)
    weight: float
    variable_data_1: Optional[float] = None
    variable_data_2: Optional[float] = None
    LEN_STEP: float = 0.65  # По умолчанию присвоено для ходьбы и бега
    M_IN_KM: int = 1000  # Константа для перевода м в км

    def get_distance(self) -> float:  # Получить дистанцию
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()  # Получаем дистанцию
        speed = self.get_mean_speed()  # Получаем среднюю скорость
        calories = self.get_spent_calories()  # Получаем каллории
        traning_type = self.__class__.__name__
        info_message = InfoMessage(traning_type, self.duration,
                                   distance, speed, calories)
        return info_message


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18  # Коэфициенты для формулы
        coeff_calorie_2 = 20
        mean_speed = self.get_mean_speed()  # Запрашиваем среднюю скорость
        duration_min = self.duration * 60  # Переводим длительность в минуты
        return (
                (coeff_calorie_1 * mean_speed - coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * duration_min
        )


@dataclass
class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    Данный класс использует variable_data_1 в которой хранится рост (height)
    """
    height: Optional[float] = None  # это "заглушка" чтобы пройти тесты.

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035  # Коэфициенты для формулы
        coeff_calorie_2 = 0.029
        mean_speed = self.get_mean_speed()  # Запрашиваем среднюю скорость
        duration_min = self.duration * 60  # Переводим длительность в минуты
        return (
            (coeff_calorie_1
             * self.weight
             + (mean_speed**2 // self.variable_data_1)
             * coeff_calorie_2 * self.weight)
            * duration_min
        )


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.
    Данный класс использует:
    variable_data_1 - для значения длинны бассейна (length_pool)
    variable_data_2 - для кол-ва проплытых бассейнов (count_pool)
    """

    LEN_STEP: float = 1.38  # Переназначили длину гребка
    length_pool: Optional[float] = None  # это "заглушка" чтобы пройти тесты.
    count_pool: Optional[float] = None  # это "заглушка" чтобы пройти тесты

    def get_mean_speed(self) -> float:
        return (
            self.variable_data_1
            * self.variable_data_2
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()  # Запросим среднюю скорость
        coeff_calorie_1 = 1.1  # Коэфициенты для формулы
        coeff_calorie_2 = 2
        return (mean_speed + coeff_calorie_1) * coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Словарь типов тренировок
    train_dict: dict[str, type[Training]] = {
        'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking
    }

    if workout_type in train_dict:
        curent_train = train_dict[workout_type]  # создаем Training
        curent_train = curent_train(*data)  # записываем данные в этот объект
        return curent_train
    else:
        print(f'Тип тренировки {workout_type} не найден',
              f'Возможные типы {train_dict.keys}')


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
