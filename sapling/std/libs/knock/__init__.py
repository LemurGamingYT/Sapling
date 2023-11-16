from requests import get

from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class
from .webResponse import WebResponse


class knock:
    type = 'knock'
    
    
    @call_decorator({'url': {'type': 'string'}}, req_vm=False)
    def _knock(self, url: String):
        return Class.from_py_cls(WebResponse(get(url.value)), url.line, url.column)
