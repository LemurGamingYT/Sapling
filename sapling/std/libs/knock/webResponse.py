from requests.exceptions import JSONDecodeError
from requests import Response
from bs4 import BeautifulSoup

from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Int, Dictionary
from sapling.error import SDecodeError


class Result:
    __name__ = 'Result'
    type = 'Result'


class WebResponse:
    __name__ = 'WebResponse'
    type = 'WebResponse'
    
    def repr(self, _) -> str:
        return f'WebResponse(status: {self._status_code.value}, url: {self._url.value})'
    
    def __init__(self, vm, response: Response) -> None:
        self._html = String(-1, -1, response.text)
        self._url = String(-1, -1, response.url)
        self._status_code = Int(-1, -1, response.status_code)

        self.response = response
        self.vm = vm

        self.soup = BeautifulSoup(response.content, 'html.parser')


    @call_decorator()
    def _to_json(self, vm):
        try:
            return Dictionary.from_py_dict(self.response.json(), *vm.loose_pos)
        except JSONDecodeError:
            vm.error(SDecodeError('Cannot convert page to JSON', vm.loose_pos))

    # @call_decorator({'name': {'type': 'string'}, 'recursive': {'type': 'bool', 'default': (Bool, False)}})
    # def _find(self, vm, name: String, recursive: Bool):
    #     return py_to_sap(self.soup.find(name.value, recursive=recursive.value), *vm.loose_pos)
    #
    # @call_decorator({'name': {'type': 'string'}, 'recursive': {'type': 'bool', 'default': (Bool, False)}})
    # def _find_all(self, vm, name: String, recursive: Bool):
    #     return py_to_sap(self.soup.find_all(name.value, recursive=recursive.value), *vm.loose_pos)
