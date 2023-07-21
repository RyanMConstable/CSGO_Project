import logging
autolog = logging.getLogger('auto_log')
addlog = logging.getLogger('add_log')

#For autolog
autolog.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt=r'%m/%d/%Y %I:%M:%S %p')
fileHandler = logging.FileHandler("auto.log", mode = "a+")
fileHandler.setFormatter(formatter)
autolog.addHandler(fileHandler)

#For addlog
addlog.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt=r'%m/%d/%Y %I:%M:%S %p')
fileHandler = logging.FileHandler("add.log", mode = "a+")
fileHandler.setFormatter(formatter)
addlog.addHandler(fileHandler)