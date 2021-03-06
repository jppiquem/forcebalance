from logging import *
import sys, re

class ForceBalanceLogger(Logger):
    """This logger starts out with a default handler that writes to stdout
    addHandler removes this default the first time another handler is added.
    This is used for forcebalance package level logging, where a logger should
    always be present unless otherwise specified. To silence, add a NullHandler
    We also by default set the log level to INFO (logging.Logger starts at WARNING)"""
    def __init__(self, name):
        super(ForceBalanceLogger, self).__init__(name)
        self.defaultHandler = RawStreamHandler(sys.stdout)
        super(ForceBalanceLogger, self).addHandler(self.defaultHandler)
        self.setLevel(INFO)
        
    def addHandler(self, hdlr):
        if self.defaultHandler:
            super(ForceBalanceLogger, self).removeHandler(self.defaultHandler)
            self.defaultHandler=False
        super(ForceBalanceLogger, self).addHandler(hdlr)
        
    def removeHandler(self, hdlr):
        super(ForceBalanceLogger, self).removeHandler(hdlr)
        if len(self.handlers)==0:
            self.defaultHandler = RawStreamHandler(sys.stdout)
            super(ForceBalanceLogger, self).addHandler(self.defaultHandler)

class RawStreamHandler(StreamHandler):
    """Exactly like output.StreamHandler except it does no extra formatting
    before sending logging messages to the stream. This is more compatible with
    how output has been displayed in ForceBalance. Default stream has also been
    changed from stderr to stdout"""
    def __init__(self, stream = sys.stdout):
        super(RawStreamHandler, self).__init__(stream)
    
    def emit(self, record):
        message = record.getMessage()
        self.stream.write(message)
        self.flush()

class RawFileHandler(FileHandler):
    """Exactly like output.FileHandler except it does no extra formatting
    before sending logging messages to the file. This is more compatible with
    how output has been displayed in ForceBalance."""
    def emit(self, record):
        message = record.getMessage()
        self.stream.write(message)
        self.flush()
        
class CleanStreamHandler(StreamHandler):
    """Similar to RawStreamHandler except it does not write terminal escape codes.
    Use this for 'plain' terminal output without any fancy colors or formatting"""
    def __init__(self, stream = sys.stdout):
        super(CleanStreamHandler, self).__init__(stream)
    
    def emit(self, record):
        message = record.getMessage()
        message = re.sub("\x1b\[[0-9][0-9]?;?[0-9]?[0-9]?m", "", message)
        self.stream.write(message)
        self.flush()
        
class CleanFileHandler(FileHandler):
    """File handler that does not write terminal escape codes and carriage returns
    to files. Use this when writing to a file that will probably not be viewed in a terminal"""
    def emit(self, record):
        message = record.getMessage()
        message = re.sub("\x1b\[[0-9][0-9]?;?[0-9]?[0-9]?m", "", message)
        message = re.sub("\r", "\n", message)
        self.stream.write(message)
        self.flush()

# set up package level logger that by default prints to sys.stdout
setLoggerClass(ForceBalanceLogger)
logger=getLogger('forcebalance')
# module level loggers should use the default logger object
setLoggerClass(Logger)
logger.setLevel(INFO)
