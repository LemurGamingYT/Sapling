from logging import (
    basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL, getLogger
)

from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, String, Nil


log_map = {
    DEBUG: 'debug',
    INFO: 'info',
    WARNING: 'warning',
    ERROR: 'error',
    CRITICAL: 'critical'
}

def log(name: str, level: int, msg: str) -> None:
    logger = getLogger(name)
    logger.setLevel(level)
    
    match log_map[level]:
        case 'debug':
            logger.debug(msg)
        case 'info':
            logger.info(msg)
        case 'warning':
            logger.warning(msg)
        case 'error':
            logger.error(msg)
        case 'critical':
            logger.critical(msg)


class Logger:
    type = 'Logger'
    
    
    _DEBUG = Int(-1, -1, DEBUG)
    _INFO = Int(-1, -1, INFO)
    _WARNING = Int(-1, -1, WARNING)
    _ERROR = Int(-1, -1, ERROR)
    _CRITICAL = Int(-1, -1, CRITICAL)
    
    
    @call_decorator(req_vm=False)
    def _init(self):
        basicConfig(level=DEBUG)
    
    @call_decorator({'msg': {'type': 'string'}}, req_vm=False)
    def _debug(self, msg: String) -> Nil:
        log(__name__, DEBUG, msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator({'msg': {'type': 'string'}}, req_vm=False)
    def _info(self, msg: String) -> Nil:
        log(__name__, INFO, msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator({'msg': {'type': 'string'}}, req_vm=False)
    def _warning(self, msg: String) -> Nil:
        log(__name__, WARNING, msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator({'msg': {'type': 'string'}}, req_vm=False)
    def _error(self, msg: String) -> Nil:
        log(__name__, ERROR, msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator({'msg': {'type': 'string'}}, req_vm=False)
    def _critical(self, msg: String) -> Nil:
        log(__name__, CRITICAL, msg.value)
        return Nil(msg.line, msg.column)
