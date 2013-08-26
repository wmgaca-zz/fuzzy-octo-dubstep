from time import time


class OctoPackage(object):
    """Base type for all packages."""

    time = None

    def __init__(self, *args, **kwargs):
        self.time = time()

        for name, value in kwargs.items():
            setattr(self, name, value)

    def get_serialized(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized):
        return pickle.loads(serialized)


class HandShake(OctoPackage):
    """Sent by user when joining a conversation."""

    user_name = ''


class GoodBye(OctoPackage):
    """Sent by user when leaving the conversation."""

    pass


class UserNew(OctoPackage):
    """Sent by server, announcing a new user joined the room."""

    user_name = ''


class UserQuit(OctoPackage):
    """Sent by server, announcing a user has left the conversation."""

    user_name = ''


class UserMessage(OctoPackage):
    """Sent by user, new message."""

    user_name = ''
    message = ''

    def to_message(self):
        return Message(user_name=self.user_name, message=self.message)


class Message(OctoPackage):
    """Sent by server, user sent a message."""

    user_name = ''
    message = ''

    def to_user_message(self):
        return UserMessage(user_name=self.user_name, message=self.message)

