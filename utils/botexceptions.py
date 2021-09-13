from discord.ext.commands import UserInputError

class BaseCustomBotError(UserInputError):
    """The base exception for this bots UserInput exceptions.
    """
    def __init__(self, *args):
        self = super().__init__(self.__name__, args)

    def __str__(self):
        return self.__name__ + str(self.args)

class InvalidStateError(BaseCustomBotError):
    """The exception type for when a user uses a command at an
    invalid state, such as no game being open or started.

    This inherits from :exc:`BaseCustomBotError`.
    """
    __name__ = "InvalidStateError"

class InvalidParameterRangeError(BaseCustomBotError):
    """The exception that's raised when one of the arguments from
    a user is out of the specified range or invalid.

    This inherits from :exc:`BaseCustomBotError`.
    """
    __name__ = "InvalidParameterRangeError"