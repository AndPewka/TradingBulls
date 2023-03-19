class NoSuchServiceError(BaseException):
    def __init__(self, service):
        self.message = f"Unable to find service {service}"

    def __str__(self):
        return self.message
