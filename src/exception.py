import sys # access information about the current Python runtime, including exception details
from src.logger import logging


def error_message_detail(error, error_detail:sys): #error -> actual error that occurred
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename # extracts the filename from the traceback object where the error occurred
    
    # Create a formatted error message string, including:
        # File name where the error occurred.
        # Line number (exc_tb.tb_lineno) in the file where the error happened.
        # Actual error message (str(error))
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )
    return error_message
    


class CustomException(Exception): # inherits from Python’s built-in Exception class
    def __init__(self,error_message, error_detail:sys): # A simple description of the error, The system’s exception information
        super().__init__(error_message) #  calls the base class (Exception) constructor to initialize the error_message
        self.error_message=error_message_detail(error_message,error_detail=error_detail) # calls the error_message_detail() function to generate a detailed error message and assigns it to self.error_message
    
    def __str__(self): # method allows the CustomException class to return the detailed error message when printed or logged
        return self.error_message
    


# This file defines a mechanism for creating 
# and raising custom exceptions with detailed error messages, 
# including information about the file and 
# line number where the error occurred. 
# The CustomException class can be used to provide more 
# detailed error logging compared to a typical exception.
    



