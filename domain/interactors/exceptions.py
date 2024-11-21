
class NoCharacterError(Exception):
    """Exception raised when no active or available character is found."""

    def __init__(self, message="No active or available character was found."):
        super().__init__(message)


class CharacterImportError(Exception):
    """Exception raised when an error occurs while importing a character."""

    def __init__(self, message="Error occurred while importing the character."):
        super().__init__(message)
