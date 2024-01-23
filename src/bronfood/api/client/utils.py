
def error_data(err_message: str) -> dict[str, str]:
    return {
        'status': 'error',
        'errorMessage': err_message
    }