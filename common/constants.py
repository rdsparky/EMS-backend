from django.db.models import TextChoices


class ApplicationMessages:
    """
    Response, error etc application messages
    """

    EMAIL_PASSWORD_INCORRECT = "Invalid Email Or Password"
    INVALID_PASSWORD = "Invalid Email Or Password"
    INVALID_EMAIL = "You are not logged in with the same email id".title()
    LOGIN_SUCCESSFULLY = "login successful".title()
    LOGOUT_SUCCESSFULLY = "Logout is successful".title()
    LOGOUT_FAILED_NO_TOKEN = "Logout Failed. No Active Login found".title()
    LOGOUT_FAILED = "Logout Failed. No Active User found".title()
    USER_NOT_ACTIVE = "User is not active".title()
    SUCCESS = "Success"
    PERMISSION_DENIED = "Permission denied for this operation.".title()
    DELETED_SUCCESS = "Object deleted successfully.".title()
