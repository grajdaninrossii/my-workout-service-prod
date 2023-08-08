class AgeValueError(Exception):
    pass


class HeightValueError(Exception):
    pass


class WeightValueError(Exception):
    pass


class MaxValueTrainError(Exception):

    def __str__(self):
        return 'Введенное количество повторений превышает допустимые значения (> 200)'
    pass


class MaxRunningValueTrainError(Exception):

    def __str__(self):
        return 'Введенное время введено с ошибкой допустимые значения! Пример нужного формата: "xx.xx"'
    pass