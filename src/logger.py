import logging # for configuring and writing log messages
import os # for creating directories and file paths
from datetime import datetime # to generate the current timestamp for the log file name


LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # generates a log file name based on the current date and time

# Let's construct the full file path where the log file will be saved. It combines:
    # The current working directory (os.getcwd()).
    # A "logs" folder.
    # The dynamically generated log file name.
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

# To ensure that the "logs" folder is created if it doesn’t exist. 
# The exist_ok=True prevents an error if the folder already exists
os.makedirs(logs_path,exist_ok=True)

# Store the full path to the log file (including both the directory and file name) in LOG_FILE_PATH
LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE)


# filename=LOG_FILE_PATH: Specifies that log messages will be written to the file defined by LOG_FILE_PATH.
# format="...": This defines the format for log messages, including:
    # %(asctime)s: The timestamp when the log entry was created.
    # %(lineno)d: The line number where the log entry was generated.
    # %(name)s: The name of the logger or module.
    # %(levelname)s: The severity level of the log (INFO, WARNING, ERROR, etc.).
    # %(message)s: The actual log message.
# level=logging.INFO: This sets the logging level to INFO, meaning only log messages with this level or higher will be recorded (e.g., INFO, WARNING, ERROR).
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# This script configures logging to write messages to a dynamically generated log file. 
# The log file is stored in a "logs" directory, 
# and the format of the log messages includes important details like timestamps 
# and the severity level of the messages.
