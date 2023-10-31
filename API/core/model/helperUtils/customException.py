class InvalidUserInput(Exception):
    def __init__(self, message):
        self.message = message

    def err_mgs(self):
        return self.message
