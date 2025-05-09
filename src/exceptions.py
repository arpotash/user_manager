class ApiError(Exception):
    def __init__(self, status_code: int = 400, message: str = "Bad request"):
        self.status_code = status_code
        self.message = message


class UserNotFound(ApiError):
    def __init__(self, user_id: int):
        super().__init__(404, f"Пользователь с id {user_id} не найден")


class UserAlreadyExist(ApiError):
    def __init__(self, name: str):
        super().__init__(409, f"Пользователь с name {name} уже существует")
