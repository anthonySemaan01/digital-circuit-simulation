class ApplicationError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotFoundException(ApplicationError):
    def __init__(self):
        self.status_code: int = 404
        self.message: str = "Requested data not found"
        super().__init__(self.message)
