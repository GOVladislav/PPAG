def headling_error_pydantic(errors: list) -> str:
    list_errors: list = []
    for err in errors:
        list_errors.append(
            ': '.join([err['loc'][0], err['msg']])
        )
    return ' | '.join(list_errors)
