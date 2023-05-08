def write_bad_row_to_file(row: list[str], error) -> None:
    with open('bad_rows.txt', 'a', encoding='utf-8') as file:
        file.write(f'{str(row)},\n{error}\n')
