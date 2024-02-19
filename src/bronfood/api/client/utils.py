
def error_data(error_message: str) -> dict[str, str]:
    return {
        'status': 'error',
        'error_message': error_message
    }


def success_data(data: dict) -> dict[str, dict]:
    return {
        'status': 'success',
        'data': data,
    }
