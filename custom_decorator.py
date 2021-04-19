from functools import wraps

from flask import Flask
from flask import jsonify

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, verify_jwt_in_request
)


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def establishment_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_establishment"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Establishment status required"), 403

        return decorator

    return wrapper


def guest_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_guest"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Guest status required"), 403

        return decorator

    return wrapper
