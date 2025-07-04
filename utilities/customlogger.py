import logging


class LoggerDemo:
    def sample_logger(self):
        # Create Logger
        logger = logging.getLogger("..\\Logs\\demo.log")
        logger.setLevel(logging.INFO)

        # Create Console Handler or file handler and set the log level

        # File Handler = To transfer logs to file
        FH = logging.FileHandler("..\\Logs\\demo.log")

        # Create formatter - How you want your logs to be formatted.
        formatter_FH = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        FH.setFormatter(formatter_FH)

        # Add console handler to logger
        # File Handler
        logger.addHandler(FH)
        return logger

