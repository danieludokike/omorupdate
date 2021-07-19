from django.contrib.auth.models import User


def is_email_taken(email):
    """CHECKS IF A PARTICULAR EMAIL ADDRESS ALREADY EXISTS"""
    if User.objects.filter(email=email).exists():
        return True
    return False


def is_username_taken(username):
    """CHECKS IF A PARTICULAR USERNAME ALREADY EXISTS"""
    if User.objects.filter(username=username).exists():
        return True
    return False


def is_field_empty(*args):
    """CHECKS IF ANY FIELD IS EMPTY"""
    for field in args:
        if field == "" or field is None:
            return True
        return False
    return "NONDETERMINISTIC"
