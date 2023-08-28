import logging

#For autolog.log file
def autologf():
    autolog = logging.getLogger('auto_log')
    autolog.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt=r'%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler("auto.log", mode = "a+")
    fileHandler.setFormatter(formatter)
    autolog.addHandler(fileHandler)
    return autolog

#For addlog
def addlogf():
    addlog = logging.getLogger('add_log')
    addlog.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt=r'%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler("add.log", mode = "a+")
    fileHandler.setFormatter(formatter)
    addlog.addHandler(fileHandler)
    return addlog