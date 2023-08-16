# Errors

not_found_error = "Game not found"
already_exists_error = "Game already exists"
game_finished = "Game already finished"
method_not_allowed = "Method not allowed"
invalid_value = "Invalid value"


def get_error_code(error_msg):
    if error_msg == not_found_error:
        return 404
    if error_msg == already_exists_error:
        return 400
    if error_msg == method_not_allowed:
        return 405
    if error_msg == game_finished:
        return 400
    if error_msg == invalid_value:
        return 400

    return 400
