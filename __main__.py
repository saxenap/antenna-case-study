import logging, logging.config
from antenna.config.logger import conf as logger_configuration



if __name__ == "__main__":
    logging.config.dictConfig(logger_configuration)

