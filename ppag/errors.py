class FormatNameError(Exception):
    ...


def write_bad_row_to_file(row: list[str], error) -> None:
    '''
        Функция записывакет данные в файл bad_rows.txt

        Параметры
        ---------
            row: list[str]
                Список с ошибочной строкой, которая не смогла преброзоваться
                в схему.
            error: Exception
                Собщение об ошибке, связанное с приобразование строки.
    '''
    with open('bad_rows.txt', 'a', encoding='utf-8') as file:
        file.write(f'{str(row)},\n{error}\n')
