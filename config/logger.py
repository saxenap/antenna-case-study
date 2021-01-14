import logging, logging.handlers

conf = dict(
    version = 1,
    disable_existing_loggers = False,
    formatters = dict(
        simple = dict(
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    ),
    handlers = dict(
        console = dict(
            **{'class': 'logging.StreamHandler'},
            level = logging.DEBUG,
            formatter = 'simple',
            stream = 'ext://sys.stdout'
        ),
        info_file_handler = dict(
            **{'class': 'logging.handlers.RotatingFileHandler'},
            level = logging.INFO,
            formatter = 'simple',
            filename = 'log/info.log',
            maxBytes = 10485760,
            backupCount = 20,
            encoding = 'utf8'
        ),
        error_file_handler = dict(
            **{'class': 'logging.handlers.RotatingFileHandler'},
            level = logging.ERROR,
            formatter = 'simple',
            filename = 'log/errors.log',
            maxBytes = 10485760,
            backupCount = 20,
            encoding = 'utf8'
        )
    ),
    loggers = dict(
        antenna = dict(
            level = logging.DEBUG,
            handlers = ['console'],
            propagate = False
        )
    ),
    root = dict(
        level = logging.NOTSET,
        handlers = ['console', 'info_file_handler', 'error_file_handler']
    )
)