"""
    sqmpy.manager
    ~~~~~

    Provides user management
"""
import bcrypt

from ..core import SQMComponent
from .constants import SECURITY_MANAGER
from .exceptions import SecurityManagerException
from .models import User

__author__ = 'Mehdi Sadeghi'


class SecurityManager(SQMComponent):
    """
    Class to deal with security and users in SQM
    """
    def __init__(self):
        super(SecurityManager, self).__init__(SECURITY_MANAGER)

    def valid_login(self, username, password):
        """
        Checks if the given password is valid for the username
        """
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return _is_correct_password(password, user.password)

        return False

    def get_user(self, user_id):
        """
        Returns the user with given id
        :param id:
        :return:
        """
        user = User.query.get(user_id)
        if user is None:
            raise SecurityManagerException('User [{user_id}] not found.'.format(user_id=user_id))
        return user

def get_password_digest(password):
    """
    Generates password digest
    :param password:
    """
    # encode is required to avoid encoding exceptions
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def _is_correct_password(password, digest):
    """
    Checks if the given password corresponds to the given digest
    :param password:
    :param digest:
    """
    return bcrypt.hashpw(password.encode('utf-8'),
                         digest.encode('utf-8')) == digest