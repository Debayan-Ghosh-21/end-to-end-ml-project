import sys
from src.logger import logging

def error_message_detail(error, error_detail: sys):
    """
    Constructs detailed error message with file name and line number
    Args:
        error: Exception object
        error_detail: sys module
    Returns:
        str: Formatted error message
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in python script [{file_name}] line number [{line_number}] error message [{str(error)}]"
    return error_message

class CustomException(Exception):
    """
    Custom exception class that logs detailed error information
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logging.error(self.error_message)

    def __str__(self):
        return self.error_message

