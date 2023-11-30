from sys import exit as sys_exit

from requests.exceptions import MissingSchema
from requests import get

from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class
from .webResponse import WebResponse
from sapling.error import SError


class SRequestError(SError):
    def __init__(self, err: MissingSchema, pos: list):
        self.err = err

        self.pos = pos

    def report(self):
        print('RequestError: Invalid url')
        sys_exit(1)


class knock:
    type = 'knock'
    
    
    @call_decorator({'url': {'type': 'string'}})
    def _knock(self, vm, url: String):
        try:
            return Class.from_py_cls(WebResponse(vm, get(url.value)), url.line, url.column)
        except MissingSchema as e:
            vm.error(SRequestError(e, vm.loose_pos))
