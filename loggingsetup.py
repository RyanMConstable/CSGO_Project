import logging

#File sets up loggers instead of using costly os calls
def setup_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a+')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.filename = log_file
    streamHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    log_setup.addHandler(streamHandler)
    return

#return dictionary of logging objects  
def logsetup():
    setup_logger('auto_log', 'auto.log')
    autolog = logging.getLogger('auto_log')
    setup_logger('add_log', 'auto.log')
    addlog = logging.getLogger('add_log')
    logdict = {}
    logdict['auto'] = autolog
    logdict['add'] = addlog
    return logdict
    