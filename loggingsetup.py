import logging
autolog = logging
autolog.basicConfig(format = '%(levelname)s: %(asctime)s %(message)s',
                    datefmt=r'%m/%d/%Y %I:%M:%S %p',
                    filename = "auto.log",
                    filemode = 'a+',
                    level = logging.INFO)
    