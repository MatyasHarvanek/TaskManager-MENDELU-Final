import db


class LoginValidationResult:
    def __init__(self, isValid, message):
        self.isValid = isValid
        self.message = message


def isUserLogedIn(session):
    return session.get('id') and session.get('username')


def isUserLoginValid(username, password):
    if db.checkIfUserExists(username=username):
        return LoginValidationResult(False, "Jméno je už zabrané")

    if len(username) > 20 or len(username) < 8:
        return LoginValidationResult(False, "Jméno musí mít alespoň 8 a méně než 20 znaků")

    # password
    if len(password) > 20 or len(password) < 8:
        return LoginValidationResult(False, "Heslo musí mít alespoň 8 a méně než 20 znaků")
    if not any(char.isupper() for char in password):
        return LoginValidationResult(False, "Heslo musí mít alespoň 1 velké písmeno")
    if not any(char.isdigit() for char in password):
        return LoginValidationResult(False, "Heslo musí mít alespoň 1 číslici")

    return LoginValidationResult(True, "")
