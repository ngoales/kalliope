from functools import wraps
from flask import request, Response

from kalliope.core.ConfigurationManager import SettingLoader

from kalliope.core.ConfigurationManager.UserLoader import UserLoader
from kalliope.core.Utils.UserContext import UserContext

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    sl = SettingLoader()
    settings = sl.settings

    user = UserContext.getUserByIdentity( username )
    if user is not None and password == user.get("restAPI_password") :
        UserContext().setUser(user)
        return True
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        sl = SettingLoader()
        settings = sl.settings
        if settings.rest_api.password_protected:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated
