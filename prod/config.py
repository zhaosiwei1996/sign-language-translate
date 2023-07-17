logsconfig = {
    "version": 1,
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "level": "DEBUG",
            "formatter": "main_formatter"
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "main_formatter"
        }
    },
    "formatters": {
        "main_formatter": {
            "format": "[%(levelname)s] %(asctime)s [%(funcName)s] %(name)s %(message)s"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file_handler", "console_handler"]
    }
}

hostip = '0.0.0.0'
listport = 5000
modelfilepath = '../train/sign-language-model.h5_1000fit_9994_058'
labalfilepath = '../train/sign-language-model.pkl'
