from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL, debug, info, warning, error, critical

from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, String, Nil


class Logger:
    type = 'Logger'
    
    _DEBUG = Int(-1, -1, DEBUG)
    _INFO = Int(-1, -1, INFO)
    _WARNING = Int(-1, -1, WARNING)
    _ERROR = Int(-1, -1, ERROR)
    _CRITICAL = Int(-1, -1, CRITICAL)
    
    
    @call_decorator({'filename': {'type': 'string', 'default': (Nil, None)}}, req_vm=False)
    def _init(self, filename: String | Nil):
        if filename.type == 'string':
            basicConfig(filename=filename.value)
        else:
            basicConfig()
    
    @call_decorator(req_vm=False)
    def _debug(self, msg: String) -> Nil:
        debug(msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator(req_vm=False)
    def _info(self, msg: String) -> Nil:
        info(msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator(req_vm=False)
    def _warning(self, msg: String) -> Nil:
        warning(msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator(req_vm=False)
    def _error(self, msg: String) -> Nil:
        error(msg.value)
        return Nil(msg.line, msg.column)
    
    @call_decorator(req_vm=False)
    def _critical(self, msg: String) -> Nil:
        critical(msg.value)
        return Nil(msg.line, msg.column)
