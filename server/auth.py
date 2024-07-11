from functools import wraps
from flask_jwt_extended import current_user

def allow(*allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = current_user
            roles = [role.name for role in user.roles]
            for role in allowed_roles:
                if role in roles:
                    return fn(*args, **kwargs)
            return {"msg": "Access Denied"}, 403
        return decorator
    return wrapper
