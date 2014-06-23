"""
    sqmpy.security
    ~~~~~~~~~~~~~~~~

    Provides user management.
"""
import bcrypt
from flask.ext.login import LoginManager

from sqmpy import app
from sqmpy.security.models import User
from sqmpy.core import SQMComponent, SQMException, core_services
from sqmpy.security.constants import SECURITY_MANAGER

__author__ = 'Mehdi Sadeghi'


class SecurityManagerException(SQMException):
    """

    """


def _get_digest(password):
    """
    Generates password digest
    """
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _is_correct_password(password, digest):
    """
    Checks if the given password corresponds to the given digest
    :param password:
    :param digest:
    """
    return bcrypt.hashpw(password, digest) == digest


class SecurityManager(SQMComponent):
    """
    Class to deal with security and users in SQM
    """
    def __init__(self):
        super(SecurityManager, self).__init__(SECURITY_MANAGER)

    def valid_login(self, email, password):
        """
        Checks if the given password is valid for the username
        """
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return _is_correct_password(password, user.password)

        return False


#Activate Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    This method will load requested user or return None
    """
    return User.query.get(user_id)


#Register the component in core
#@TODO: This should be dynamic later
core_services.register(SecurityManager())