from email_validator import validate_email, EmailNotValidError

def is_email_valid(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
