from functools import wraps

from src.custom_exceptions import NotEnoughRightsError


def admin_path(f):
    @wraps(f)
    def wrapper(user, *args, **kwargs):
        if not user.is_admin:
            raise NotEnoughRightsError("Only admin user can access this endpoint")
        f(*args, **kwargs)

    return wrapper
