class ErrorHandler:
    status: str
    message: str
    additionalInfo: str

    def __init__(self, status, message, additional_info):
        self.status = status
        self.message = message
        self.additionalInfo = additional_info

    def report_error(self):
        return {'status': self.status, 'message': self.message, 'details': self.additionalInfo}

