

class Error(Exception):
    pass



class UserNotFoundError(Error):
    
    def __init__(self, message: str = "User not found!") -> None:
        super().__init__(message)


class UserIsNotLoggedInError(Error):
    
    def __init__(self, message: str = "User is not logged in!") -> None:
        super().__init__(message)


class InvalidTokenError(Error):
    
    def __init__(self, message: str = "Invalid Token!") -> None:
        super().__init__(message)


